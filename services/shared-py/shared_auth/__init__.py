import os
import time
import logging
from typing import Dict, Any

import jwt
import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

security = HTTPBearer()

# Simple Cache for JWKS
_jwks_cache: Dict[str, Any] = None
_jwks_last_fetch = 0
_CACHE_TTL = 3600 # 1 hour

def get_keycloak_url() -> str:
    url = os.getenv("ConnectionStrings__keycloak")
    if not url:
        url = os.getenv("services__keycloak__http__0")
    if not url:
        url = os.getenv("services__keycloak__https__0")
    if not url:
        url = "http://localhost:8080"
    return url.rstrip('/')

async def get_jwks(realm: str) -> dict:
    global _jwks_cache, _jwks_last_fetch
    now = time.time()
    
    if _jwks_cache and (now - _jwks_last_fetch) < _CACHE_TTL:
        return _jwks_cache
        
    base_url = get_keycloak_url()
    certs_url = f"{base_url}/realms/{realm}/protocol/openid-connect/certs"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(certs_url, timeout=10.0)
            response.raise_for_status()
            _jwks_cache = response.json()
            _jwks_last_fetch = now
            return _jwks_cache
    except Exception as e:
        logger.error(f"Failed to fetch JWKS from {certs_url}: {e}")
        raise HTTPException(status_code=500, detail="Identity provider keys unavailable")

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = credentials.credentials
    realm = "app"
    
    try:
        unverified_header = jwt.get_unverified_header(token)
        jwks = await get_jwks(realm)
        
        # Find the matching key in JWKS
        rsa_key = {}
        for key in jwks.get("keys", []):
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break
                
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid token: no matching key found")
            
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)
        
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False} # Keep it simple
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Token validation failed")
