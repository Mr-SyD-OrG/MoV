from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("MrSyD")


@routes.get("/file/{chat_id}/{message_id}")
async def handle_request(req: web.Request) -> web.Response:
    chat_id = int(req.match_info["chat_id"])
    message_id = int(req.match_info["message_id"])

    try:
        message = await client.get_messages(chat_id, message_id)
        if not message or not message.media:
            return web.Response(status=404, text="Media not found.")

        size = message.file.size
        offset = req.http_range.start or 0
        limit = req.http_range.stop or size
        length = limit - offset

        ip = get_requester_ip(req)
        if not allow_request(ip):
            return web.Response(status=429, text="Rate limited.")

        log.info(f"Streaming message {message_id} to {ip}")

        body = transfer.download(
            message.media,
            file_size=size,
            offset=offset,
            limit=limit
        )

        return web.Response(
            status=206 if offset else 200,
            body=body,
            headers={
                "Content-Type": message.file.mime_type or "application/octet-stream",
                "Content-Range": f"bytes {offset}-{limit - 1}/{size}",
                "Content-Length": str(length),
                "Accept-Ranges": "bytes",
            },
        )

    except Exception as e:
        return web.Response(status=500, text=f"Error: {str(e)}")

