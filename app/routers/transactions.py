import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# ── Modelos ────────────────────────────────────────────────────────────────────

class TransactionRequest(BaseModel):
    amount: float = Field(..., gt=0, examples=[150.00])
    currency: str = Field(default="BOB", examples=["BOB", "USD"])
    sender: str = Field(..., examples=["user-001"])
    receiver: str = Field(..., examples=["merchant-007"])
    description: str | None = Field(default=None, examples=["Pago servicio internet"])


class Transaction(BaseModel):
    id: str
    amount: float
    currency: str
    sender: str
    receiver: str
    description: str | None
    status: Literal["pending", "completed", "failed"]
    created_at: str


# ── Base de datos en memoria (demo) ───────────────────────────────────────────

_db: dict[str, Transaction] = {
    "txn-001": Transaction(
        id="txn-001",
        amount=250.00,
        currency="BOB",
        sender="user-001",
        receiver="merchant-007",
        description="Pago agua potable",
        status="completed",
        created_at="2026-04-30T10:15:00Z",
    ),
    "txn-002": Transaction(
        id="txn-002",
        amount=99.50,
        currency="BOB",
        sender="user-042",
        receiver="merchant-003",
        description="Recarga saldo",
        status="completed",
        created_at="2026-04-30T11:30:00Z",
    ),
}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[Transaction])
def list_transactions():
    return list(_db.values())


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str):
    txn = _db.get(transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.post("/", response_model=Transaction, status_code=201)
def create_transaction(body: TransactionRequest):
    txn_id = f"txn-{uuid.uuid4().hex[:8]}"
    txn = Transaction(
        id=txn_id,
        amount=body.amount,
        currency=body.currency,
        sender=body.sender,
        receiver=body.receiver,
        description=body.description,
        status="completed",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    _db[txn_id] = txn
    return txn
