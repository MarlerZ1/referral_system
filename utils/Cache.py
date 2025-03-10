import json

from asgiref.sync import sync_to_async
from django.core.cache import cache

from referral_system.settings import CACHE_TIMEOUT


async def get_cached_code(email=None, owner=None):
    if not email and not owner:
        raise ValueError("One of the params must be set")


    from referral.models import ReferralCode
    from referral.serializers import ReferralCodeSerializer
    from authorization.models import User

    cached_data = await sync_to_async(cache.get)(email)

    if cached_data:
        data = json.loads(cached_data)
        return ReferralCode(**data)

    try:
        if not owner:
            owner = await User.objects.aget(email=email if email else owner.email)

        code_object = await ReferralCode.objects.aget(owner=owner)
        serialized = ReferralCodeSerializer(code_object).data
        await sync_to_async(cache.set)(owner.email, json.dumps(serialized), CACHE_TIMEOUT)
        return code_object
    except:
        return None
