from aiogram import Router

from . import admin
from . import user


def get_routers() -> list[Router]:
    return [
        admin.router,
        user.router
    ]
