from typing import Optional

from pydantic import BaseModel


class PhoneInfo(BaseModel):
    success: bool
    phone: Optional[str]
    message: Optional[str]
