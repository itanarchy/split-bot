from .base import PublicSplitMethod


class GenerateTonProofPayload(
    PublicSplitMethod[str],
    api_method="/ton-proof/generate_payload",
    returning=str,
    response_data_key=["payload"],
):
    pass
