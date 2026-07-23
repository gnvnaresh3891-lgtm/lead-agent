import pytest
from app.core.redis_client import RedisClient, get_redis_client


@pytest.mark.asyncio
async def test_redis_client_connect_and_fallback(redis_client):
    """Test RedisClient connection fallback behavior."""
    assert redis_client is not None
    # Verify client is either connected to Redis server or operating in fallback queue mode
    assert isinstance(redis_client.is_fallback, bool)


@pytest.mark.asyncio
async def test_redis_client_push_pop_fifo(redis_client):
    """Test RedisClient LPUSH and pop FIFO functionality."""
    q_name = "test_queue_fifo"
    item1 = {"id": "msg_1", "data": "first"}
    item2 = {"id": "msg_2", "data": "second"}

    await redis_client.push_signal(q_name, item1)
    await redis_client.push_signal(q_name, item2)

    popped1 = await redis_client.pop_signal(q_name, timeout=0.1)
    popped2 = await redis_client.pop_signal(q_name, timeout=0.1)

    assert popped1["id"] == "msg_1"
    assert popped2["id"] == "msg_2"


@pytest.mark.asyncio
async def test_redis_client_queue_len(redis_client):
    """Test RedisClient queue length tracking."""
    q_name = "test_queue_len"
    assert await redis_client.get_queue_len(q_name) == 0

    for i in range(5):
        await redis_client.push_signal(q_name, {"idx": i})

    assert await redis_client.get_queue_len(q_name) == 5

    await redis_client.pop_signal(q_name, timeout=0.1)
    assert await redis_client.get_queue_len(q_name) == 4


@pytest.mark.asyncio
async def test_redis_client_sadd_sismember(redis_client):
    """Test RedisClient set operations (SADD / SISMEMBER)."""
    set_name = "test_set"
    member = "msg_1001"

    added = await redis_client.sadd(set_name, member)
    assert added == 1

    is_mem = await redis_client.sismember(set_name, member)
    assert is_mem is True

    # Adding duplicate member returns 0
    duplicate_add = await redis_client.sadd(set_name, member)
    assert duplicate_add == 0


@pytest.mark.asyncio
async def test_redis_client_dlq(redis_client):
    """Test RedisClient move_to_dlq functionality."""
    q_name = "test_queue"
    payload = {"failed_msg": "corrupt_data"}

    await redis_client.move_to_dlq(q_name, payload, error_reason="SchemaValidationError")

    dlq_item = await redis_client.pop_signal("dlq:signals", timeout=0.1)
    assert dlq_item is not None
    assert dlq_item["payload"] == payload
    assert dlq_item["error_reason"] == "SchemaValidationError"


@pytest.mark.asyncio
async def test_redis_client_clear(redis_client):
    """Test RedisClient clear method resets all state."""
    q_name = "test_queue_clear"
    await redis_client.push_signal(q_name, {"test": "val"})
    assert await redis_client.get_queue_len(q_name) == 1

    await redis_client.clear()
    assert await redis_client.get_queue_len(q_name) == 0
