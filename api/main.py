from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from logger import log_audit
import tools.calc1040 as calc1040
import tools.docs as docs

app = FastAPI(title="TaxCRM API")

# OAuth2 placeholder (can integrate with Auth0/Okta/Keycloak later)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Welcome to TaxCRM API"}

@app.post("/calc1040")
@log_audit
async def calculate_1040(income: float, status: str, token: str = Depends(oauth2_scheme)):
    return calc1040.calc_1040(income, status)

@app.get("/presign")
@log_audit
async def presign(file_name: str, token: str = Depends(oauth2_scheme)):
    return docs.generate_presign_url(file_name)
