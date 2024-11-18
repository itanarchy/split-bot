from app.utils.key_builder import StorageKey


class TcRecordKey(StorageKey, prefix="tc_records"):
    telegram_id: int
    key: str


class UserKey(StorageKey, prefix="users"):
    key: str
