from pydantic import BaseModel

# POST するアイテム


class PostItem(BaseModel):
    image_base64: str
    link_url: str
