azure_subscription_id = "ad42a479-91b2-4d5c-90cd-f70b4f454593"
location              = "centralus"
resource_group_name   = "aw-rg-2"
environment           = "dev"


# az functionapp deployment source config-zip -g aw-rg-2-dev -n fastapi_function --src ./test_app.zip