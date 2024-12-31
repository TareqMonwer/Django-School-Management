from django.urls import reverse
from django_school_management.accounts.models import User
from typing import List, Dict, Any, Set


class MenuService:
    def __init__(self, menu_config: Dict[str, Any]):
        """
        Initialize the MenuService with the given configuration.
        """
        self.menu_config = menu_config

    def get_user_groups(self, user: User) -> Set[str]:
        """
        Retrieve the groups of the user as a set.
        """
        return set(user.groups.values_list("name", flat=True))

    def add_urls_to_menu(
        self,
        menu_items: List[Dict[str, str]],
        urls: List[Dict[str, str]],
        added_urls: Set[str],
    ) -> None:
        """
        Add reversed URLs and titles to the menu_items list, ensuring only unique URLs are added.
        """
        for url in urls:
            reversed_url = reverse(url["name"])
            if reversed_url not in added_urls:
                menu_items.append({"url": reversed_url, "title": url["title"]})
                added_urls.add(reversed_url)

    def get_menu_items(self, section: str, user: User) -> List[Dict[str, str]]:
        """
        Retrieve menu items for a given section based on the user's groups.
        """
        user_groups = self.get_user_groups(user)
        menu_items = []
        added_urls = set()

        if section not in self.menu_config:
            return menu_items

        for entry in self.menu_config[section]:
            if user_groups & entry["groups"]:
                self.add_urls_to_menu(menu_items, entry["urls"], added_urls)

        return menu_items
