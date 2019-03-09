import vk
import time


class VKParser:
    def __init__(self, **kwargs):
        self._MAX_POSTS_PER_QUERY = 100
        self._config = kwargs
        session = vk.AuthSession(app_id=self._config['app_id'],
                                 user_login=self._config['login'],
                                 user_password=self._config['password'])
        self._api = vk.API(session, v='5.73', lang='ru')

    def post_iter(self, offset=0, count=-1, interval=2):
        group_id = self._get_group_id(self._config['group_name'])
        if group_id == -1:
            raise ValueError('Group not found.')
        while count != 0:
            posts_chunk = self._get_posts_chunk(group_id, offset, self._MAX_POSTS_PER_QUERY)
            if len(posts_chunk) == 0:
                break
            for post in posts_chunk:
                if self._is_ad_post(post):
                    continue
                if count == 0:
                    break
                count -= 1
                text = post['text'].replace('\n', ' ')
                yield text
            offset += len(posts_chunk)
            time.sleep(interval)

    def dump_posts(self, filename):
        posts = [post for post in self.post_iter()]
        with open(filename, 'w', encoding='utf8') as file:
            print(*posts, sep='\n', file=file)

    def _get_group_id(self, group_name):
        response = self._api.groups.getById(group_id=group_name)
        if len(response) == 0:
            return -1
        return response[0]['id']

    def _get_posts_chunk(self, group_id, offset, count):
        response = self._api.wall.get(owner_id=-group_id,
                                      offset=offset,
                                      count=count)
        return response['items']

    @staticmethod
    def _is_ad_post(post):
        return post.get('is_pinned', 0) != 0 and post.get('marked_as_ad', 0) != 0
