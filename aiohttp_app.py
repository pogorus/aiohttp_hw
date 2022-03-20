from aiohttp import web
from database import db, AdModel
from asyncpg.exceptions import UniqueViolationError
import json

import database

app = web.Application()


class AdView(web.View):
    async def get_all(self):
        ad_list = []
        all_ad = await db.all(AdModel.query)
        for ad in all_ad:
            ad_list.append(ad.to_dict())
        ad_json = json.dumps(ad_list)
        return web.json_response(ad_json)

    async def get(self):
        ad_id = int(self.request.match_info['ad_id'])
        ad = await AdModel.get(ad_id)
        if ad is None:
            return web.json_response({'error': 'not found'}, status=404)
        ad_data = ad.to_dict()
        return web.json_response(ad_data)

    async def post(self):
        json_data = await self.request.json()
        try:
            new_ad = await AdModel.create(**json_data)
        except UniqueViolationError:
            return web.json_response({'error': 'already exists'}, status=300)
        return web.json_response(new_ad.to_dict())

    async def update(self):
        ad_id = int(self.match_info['ad_id'])
        ad = await AdModel.get(ad_id)
        if ad is None:
            return web.json_response({'error': 'not found'}, status=404)
        json_data = await self.json()
        for key in json_data.keys():
            setattr(ad, key, json_data.get(key))
        await ad.update(**json_data).apply()
        updated_ad = await AdModel.get(ad_id)
        return web.json_response(updated_ad.to_dict())

    async def delete_ad(self):
        ad_id = int(self.match_info['ad_id'])
        ad = await AdModel.get(ad_id)
        await ad.delete()
        return web.json_response({f'Ad #{ad_id}': 'deleted'}, status=200)


app.add_routes([
    web.post('/ad', AdView),
    web.get('/ad/{ad_id:\d+}', AdView),
    web.get('/all_ad', AdView.get_all),
    web.delete('/ad/{ad_id:\d+}', AdView.delete_ad),
    web.patch('/ad/{ad_id:\d+}', AdView.update),
])


async def init_orm(app):
    await db.set_bind(database.PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()

app.cleanup_ctx.append(init_orm)

web.run_app(app, port=8080)
