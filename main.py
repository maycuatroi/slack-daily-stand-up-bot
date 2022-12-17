"""
Create one time trigger, auto trigger when https request is received.
"""
import requests
import sentry_sdk
from fastapi import FastAPI

from daily_stand_up_bot import config
from daily_stand_up_bot.controllers.slack_controller import SlackController
from daily_stand_up_bot.controllers.user_controller import UserController

sentry_sdk.init(
    dsn=config.SENTRY_DNS,
    traces_sample_rate=1.0,
)

app = FastAPI()


@app.post("/daily")
async def daily():
    user_controller = SlackController()
    users = user_controller.get_all_users()

    return {"message": "Daily"}


# handle slack oauth when user install app
@app.get("/slack/oauth")
async def slack_oauth(code: str, state: str):
    """
    Handle slack oauth when user install app
    Exchanging a temporary authorization code for an access token
    If all's well, a user goes through the Slack app installation UI and okays your app with all the scopes that it requests. After that happens, Slack redirects the user back to your specified Redirect URL.

    Parse the HTTP request that lands at your Redirect URL for a code field. That's your temporary authorization code, which expires after ten minutes.

    Check the state parameter if you sent one along with your initial user redirect. If it doesn't match what you sent, consider the authorization a forgery.

    Now you just have to exchange the code for an access token. You'll do this by calling the oauth.v2.access method:

    curl -F code=1234 -F client_id=3336676.569200954261 -F client_secret=ABCDEFGH https://slack.com/api/oauth.v2.access
    Note: If you initiate an install with the v2/authorize URL, it must be completed with oauth.v2.access, not the old oauth.access method.

    After you complete your access call, Slack sends you an HTTP request response containing an access token. It looks like this:

    {
        "ok": true,
        "access_token": "xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy",
        "token_type": "bot",
        "scope": "commands,incoming-webhook",
        "bot_user_id": "U0KRQLJ9H",
        "app_id": "A0KRD7HC3",
        "team": {
            "name": "Slack Softball Team",
            "id": "T9TK3CUKW"
        },
        "enterprise": {
            "name": "slack-sports",
            "id": "E12345678"
        },
        "authed_user": {
            "id": "U1234",
            "scope": "chat:write",
            "access_token": "xoxp-1234",
            "token_type": "user"
        }
    }
    If you requested scopes for a user token, you'll find them with a user access token under the authed_user property.
    """

    client_secret = config.CLIENT_SECRET
    client_id = config.CLIENT_ID
    res = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    auth_response = res.json()

    # save auth response to database
    user_controller = UserController()
    authed_user = auth_response["authed_user"]
    authed_user_id = authed_user["id"]
    user_controller.save_user(authed_user_id, auth_response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080, log_level="info")
