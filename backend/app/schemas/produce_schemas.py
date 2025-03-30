from pydantic import BaseModel

class AddProduceRequest(BaseModel):
    farmer_name: str
    crop_name: str
    quantity: int
    location: str
    account: str
    private_key: str
