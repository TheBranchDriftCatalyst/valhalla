from fastapi import FastAPI, applications
# from fastapi.openapi.docs import get_swagger_ui_html
# from fastapi.staticfiles import StaticFiles

app = FastAPI()
    
@app.get('/health')
def health(self):
    return {'status': 'ok'}

# custom swagger ui???  
# assets_path = os.getcwd() + "/swagger-ui-assets"
# if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
#     app.mount("/assets", StaticFiles(directory=assets_path), name="static")
#     def swagger_monkey_patch(*args, **kwargs):
#         return get_swagger_ui_html(
#             *args,
#             **kwargs,
#             swagger_favicon_url="",
#             swagger_css_url="/assets/swagger-ui.css",
#             swagger_js_url="/assets/swagger-ui-bundle.js",
#         )
#     applications.get_swagger_ui_html = swagger_monkey_patch
