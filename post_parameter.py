from pydantic import BaseModel

# POST するアイテム


class PostCredential(BaseModel):
    mail_address: str
    password: str


class PostRefreshToken(BaseModel):
    refresh_token: str


class PostItem(BaseModel):
    image_base64: str
    link_url: str
