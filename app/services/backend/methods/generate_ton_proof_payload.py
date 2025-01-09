from .base import SplitMethod


class GenerateTonProofPayload(
    SplitMethod[str],
    api_method="/ton-proof/generate_payload",
    returning=str,
    response_data_key=["message", "payload"],
):
    pass
