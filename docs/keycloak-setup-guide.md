# Keycloak Setup Guide

This guide explains how to configure Keycloak for use with the Aspire Python Microservices template.

## 1. Aspire Orchestration Configuration

In `apphost.cs`, Keycloak is initialized with admin credentials provided as parameters:

```csharp
var username = builder.AddParameter("username");
var password = builder.AddParameter("password", secret: true);

var keycloak = builder.AddKeycloak("keycloak", 8080, username, password)
    .WithDataVolume()
    .WithOtlpExporter();
```

When you first run the application, Aspire will prompt you to provide values for these parameters. Use these credentials to log into the Keycloak Admin Console.

## 2. Accessing the Admin Console

1. Run the Aspire project using `aspire run`.
2. Open the Aspire Dashboard.
3. Find the `keycloak` resource and click its endpoint link (usually `http://localhost:8080`).
4. Log in using the `username` and `password` you provided to Aspire.

## 3. Create the 'app' Realm

1. In the top-left corner, click the dropdown menu (it usually says **Master**) and select **Create Realm**.
2. Enter `app` as the **Realm name**.
3. Click **Create**.

## 4. Create the 'frontend' Client

1. Ensure the `app` realm is selected.
2. Click **Clients** in the left sidebar.
3. Click **Create client**.
4. Configure the following settings:
   - **Client type**: `OpenID Connect`
   - **Client ID**: `frontend`
   - **Name**: `Vite Frontend` (optional)
5. Click **Next**.
6. Ensure **Standard flow** is enabled.
7. Set **Access settings**:
   - **Root URL**: The URL where your frontend runs (e.g., `https://localhost:12345`).
   - **Valid redirect URIs**: `*` (for development) or specific frontend URLs.
   - **Web origins**: `*` (highly recommended for development to avoid CORS issues).
8. Click **Save**.

## 5. Create a User

1. In the left sidebar, click **Users**.
2. Click **Add user**.
3. Enter a **Username** (e.g., `testuser`).
4. Click **Create**.
5. Go to the **Credentials** tab.
6. Click **Set password**.
7. Enter a password and turn off **Temporary**.
8. Click **Save**.

## 6. Verification

1. Go to the Vite Frontend via the Aspire Dashboard.
2. You should be redirected to the Keycloak login screen.
3. Log in with the user you just created.
4. If successful, you will be redirected back to the app, and the backend services will accept your authenticated requests.
