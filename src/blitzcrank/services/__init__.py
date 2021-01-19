from typing import Union
import discord
from discord.ext import commands
from discord.utils import get

import logging

logger: logging.Logger = logging.getLogger(__name__)


async def grant_member_role(ctx: commands.Context, role_name) -> None:
    member = ctx.message.author
    role = get(member.guild.roles, name=role_name)
    await member.add_roles(role)
    if not await member_has_role(role, member):
        raise MemberRoleException(f"Unable to grant role {role_name} to {member.name}")


async def member_has_role(role, member: discord.Member) -> bool:
    member_roles = list(role.name for role in member.roles)
    if role.name not in member_roles:
        return False
    return True


class MemberRoleException(Exception):
    pass
