import aiohttp
import asyncio


class ApiClient:

    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.session = aiohttp.ClientSession()

    async def _call(self, http_method, api_method, response_type=None, *args, **kwargs):
        request_method = getattr(self.session, http_method)
        response = await request_method(f'{self.host}/{api_method}', *args, **kwargs)
        if response_type == 'json':
            response = await response.json(content_type=None)
        return response

    async def create_ad(self, title, description, owner):
        return await self._call('post', 'ad', response_type='json', json={'title': title,
                                                                          'description': description,
                                                                          'owner': owner,
                                                                          })

    async def get_ad(self, ad_id):
        return await self._call('get', f'ad/{ad_id}', response_type='json')

    async def get_all_ad(self):
        return await self._call('get', 'all_ad', response_type='json')

    async def delete_ad(self, ad_id):
        return await self._call('delete', f'ad/{ad_id}')

    async def update_ad(self, ad_id, title, description, owner):
        return await self._call('patch', f'ad/{ad_id}', response_type='json', json={'title': title,
                                                                                    'description': description,
                                                                                    'owner': owner,
                                                                                    })

    async def close(self):
        await self.session.close()


async def main():
    client = ApiClient()
    print(await client.create_ad('title1', 'desc1', 'owner1'))
    print(await client.create_ad('title2', 'desc2', 'owner2'))
    print(await client.create_ad('title3', 'desc3', 'owner3'))
    print(await client.get_all_ad())
    print(await client.update_ad(2, 'title20', 'desc20', 'owner20'))
    print(await client.get_ad(2))
    print(await client.delete_ad(1))
    print(await client.get_all_ad())
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())
