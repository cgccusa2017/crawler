

# TODO: this class will handles crawler settings for the url that requires login information.
class LoginModule():


    def get_cookies(self, url, login_func=None):
        """
        This function returns the cookie after logged in of the url
        :param url:
        :param crawler_settings:
        :return: cookies to access the url without logging in again
        """

        if login_func:
            return login_func(url)
        return None

