import asyncio

import httpx
import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'cookie': 'ttwid=1%7ClKjt-7boLVhQW8fUvz5RCz_2Tksp7LI9sXZ27C4bX_4%7C1736756975%7C451727599e49dce9b317040420a3ba25bb0b51d4d74a09f4f663cf3194820292; UIFID_TEMP=c4a29131752d59acb78af076c3dbdd52744118e38e80b4b96439ef1e20799db0eff9beb6f9cab0e0fce22e28819d64e91f14dc0c732bd424d2c3f801061fe2f4b740de3d358064b44c13f5ed7177b4e2; hevc_supported=true; xgplayer_user_id=787898530982; fpk1=U2FsdGVkX19wfQJNy7J57zqX4nFcvwccqLq/fk2emzoCh350PiaQ4QdGMLfOpp6frnEUeOs9ehWMUqJKvJemSA==; fpk2=f51bb482c660d0eeadd1f058058a2b35; bd_ticket_guard_client_web_domain=2; UIFID=c4a29131752d59acb78af076c3dbdd52744118e38e80b4b96439ef1e20799db0eff9beb6f9cab0e0fce22e28819d64e9d84aa638069d7210c5ebf7a2189ffd7556e724dfd5bdc9cbdfebb4b211d70afd7a8a929df3f88b6abf7988ff2624e85c19863556eaa7cd3d42ce262f36c5cf9df2cdef40f64cafc8d1cd484b1283691fcedff51709ff3153e0a427957f34fe280c1287ed18e707ea96015706d2e1d074; is_staff_user=false; SelfTabRedDotControl=%5B%5D; store-region=cn-he; store-region-src=uid; xgplayer_device_id=34182579705; dy_swidth=1920; dy_sheight=1080; is_dash_user=1; live_use_vvc=%22false%22; my_rd=2; __live_version__=%221.1.2.8371%22; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0EyOTglMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E2NzclMkMlMjJ3aWR0aCUyMiUzQTI5OCUyQyUyMmhlaWdodCUyMiUzQTY3NyUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0ExJTJDJTIydXNlckFnZW50JTIyJTNBJTIyTW96aWxsYSUyRjUuMCUyMChXaW5kb3dzJTIwTlQlMjAxMC4wJTNCJTIwV2luNjQlM0IlMjB4NjQpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGMTMzLjAuMC4wJTIwU2FmYXJpJTJGNTM3LjM2JTIyJTdE; s_v_web_id=verify_m8bn0yqf_cIYObpd5_EaIk_4xsZ_AOE9_0RLUORCKxNxR; __security_mc_1_s_sdk_crypt_sdk=f9f5ca59-4c38-b1f3; __security_mc_1_s_sdk_cert_key=4060aecf-4733-88e6; passport_csrf_token=14fefd51434331c69cdd7e01cc5fdf36; passport_csrf_token_default=14fefd51434331c69cdd7e01cc5fdf36; passport_assist_user=CkH0XhmDQ01KC7QkubfJkq7yEkigtEJv3JYqlMNafTknCT4qRyljeCcPC7NLrTkhjEjRucJyKfnqlauvlBMd95h1ZhpKCjx9WKn1THpRrHh-0FB-2Iq1RoQm3FnCecqCqPbhgEeWERtUc4LbwpgvkNNueS_F3xhgWYD0-MpGuO6WVfQQnKvsDRiJr9ZUIAEiAQPK8VpE; n_mh=hMt7oFAjIcJDtL2CVbRgS5TbvMr2PBxEiuJyDLHS6dc; sid_guard=0559d5698c5d618608001dbc01af6f54%7C1742295037%7C5184000%7CSat%2C+17-May-2025+10%3A50%3A37+GMT; uid_tt=d33668062c165d035a978e9ba9d954e3; uid_tt_ss=d33668062c165d035a978e9ba9d954e3; sid_tt=0559d5698c5d618608001dbc01af6f54; sessionid=0559d5698c5d618608001dbc01af6f54; sessionid_ss=0559d5698c5d618608001dbc01af6f54; sid_ucp_v1=1.0.0-KGMxYTlhZTUxNTgwNjFiMWY4MTkxOTc4YThlZGY0NzY1MjY4NGVmMDgKIQjDrNDUwfXABBD9n-W-BhjvMSAMMObShuYFOAdA9AdIBBoCaGwiIDA1NTlkNTY5OGM1ZDYxODYwODAwMWRiYzAxYWY2ZjU0; ssid_ucp_v1=1.0.0-KGMxYTlhZTUxNTgwNjFiMWY4MTkxOTc4YThlZGY0NzY1MjY4NGVmMDgKIQjDrNDUwfXABBD9n-W-BhjvMSAMMObShuYFOAdA9AdIBBoCaGwiIDA1NTlkNTY5OGM1ZDYxODYwODAwMWRiYzAxYWY2ZjU0; login_time=1742295037710; _bd_ticket_crypt_cookie=361f5c73dc53290c12c1ab32b4309027; __security_mc_1_s_sdk_sign_data_key_web_protect=165931ed-4381-a0b8; __security_server_data_status=1; download_guide=%223%2F20250324%2F0%22; publish_badge_show_info=%220%2C0%2C0%2C1743950699363%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.372%7D; EnhanceDownloadGuide=%220_0_2_1744031550_0_0%22; strategyABtestKey=%221744075597.448%22; biz_trace_id=fdf42aaf; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; __ac_signature=_02B4Z6wo00f01vAaNwAAAIDAE9XHlBEA51bwOjOAANv.5d; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAX92IFqsPH_-BclD5KVNocsgyCm1Sz93Xc8xEwmOJjLM2khnlWIjx-Yf-Ek7P0ql3%2F1744128000000%2F0%2F1744081878277%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS283VDhDTHhKWXdueWk5SXJPdXZMcWV2bUd3UEZzeWVTdkpMcnA0aG5Sb1hreERqQlBILzhnUldGNE9WVzgySFpzU2gyeHRkd2dDSWgxQTV3RnJvVjQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; WallpaperGuide=%7B%22showTime%22%3A1743418853830%2C%22closeTime%22%3A0%2C%22showCount%22%3A3%2C%22cursor1%22%3A47%2C%22cursor2%22%3A14%2C%22hoverTime%22%3A1742207755077%7D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAX92IFqsPH_-BclD5KVNocsgyCm1Sz93Xc8xEwmOJjLM2khnlWIjx-Yf-Ek7P0ql3%2F1744128000000%2F0%2F1744083833787%2F0%22; IsDouyinActive=false; passport_fe_beating_status=false; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; odin_tt=fd3e72df6d9c7c39a49fa879e13a60b0ad8f99bc6261754044eb8a000104600a03eeac31e9097dcc25effe6f35685e79063935ed9df327669c43e2204489f55c',
}
save_path = "./download/douyin/兔兔兔奶糖_7489891376180628790.mp4"
url = "https://www.douyin.com/aweme/v1/play/?video_id=v0d00fg10000cvon1evog65mfcmnn080&line=0&file_id=970ed300ec8e43cb9f07d7db394920ce&sign=f87c4a116bcbfddaae7d8b4f13b94446&is_play_url=1&source=PackSourceEnum_AWEME_DETAIL"
# response = requests.get(url, headers=headers, timeout=30)
# print(response.text)

async def main():
   async with httpx.AsyncClient( headers=headers, follow_redirects=True) as client:
        async with client.stream("GET", url=url) as response:
            with open(save_path, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)


        # response = await client.get(url=url)
        # print(response.text)
if __name__ == '__main__':
    asyncio.run(main())