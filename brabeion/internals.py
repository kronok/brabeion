from collections import defaultdict

from brabeion.base import Badge


class BadgeCache(object):
    """
    This is responsible for storing all badges that have been registered, as
    well as providing the pulic API for awarding badges.
    
    This class should not be instantiated multiple times, if you do it's your
    fault when things break, and you get to pick up all the pieces.
    """
    def __init__(self):
        self._event_registry = defaultdict(list)
        self._registry = {}
    
    def register(self, badge):
        # We should probably duck-type this, but for now it's a decent sanity
        # check.
        assert issubclass(badge, Badge)
        badge = badge()
        self._registry[badge.slug] = badge
        for event in badge.events:
            self._event_registry[event].append(badge)
    
    def possibly_award_badge(self, event, **state):
        for badge in self._registry[event]:
            badge.possibly_award(**state)


class AwardedBadge(object):
    def __init__(self, slug, level, user):
        self.slug = slug
        self.level = level
        self.user = user
        self._badge = badges._registry[slug]
    
    @property
    def name(self):
        return self._badge.levels[self.level].name
    
    @property
    def description(self):
        return self._badge.levels[self.level].description
    
    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)


badges = BadgeCache()