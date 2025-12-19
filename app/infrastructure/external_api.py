from fastapi import HTTPException
import httpx

class ExternalApiClient:

    def __init__(self):
        self.base_url = 'https://jsonplaceholder.typicode.com'

    async def get_all_posts(self):
        async with httpx.AsyncClient() as client:
            try:
                
                response = await client.get(f'{self.base_url}/posts', timeout=10.0);

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.text
                    )
            
                return response.json()
            
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Timeout")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
    async def get_post_by_id(self, post_id: int):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f'{self.base_url}/posts/{post_id}', timeout=10.0);
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.text
                    )
                
                return response.json()
            
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Timeout")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
            
external_api_client = ExternalApiClient()