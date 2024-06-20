class AWPlaces:
    def __init__(self, id, displayName, types, location, viewport, rating, regularOpeningHours, utcOffsetMinutes,
                 userRatingCount, currentOpeningHours, primaryType, accessibilityOptions):
        self.id = id
        self.displayName = displayName
        self.types = types
        self.location = location
        self.viewport = viewport
        self.rating = rating
        self.regularOpeningHours = regularOpeningHours
        self.utcOffsetMinutes = utcOffsetMinutes
        self.userRatingCount = userRatingCount
        self.currentOpeningHours = currentOpeningHours
        self.primaryType = primaryType
        self.accessibilityOptions = accessibilityOptions

    def to_dict(self):
        return {
            "id": self.id,
            "displayName": self.displayName,
            "types": self.types,
            "location": self.location,
            "viewport": self.viewport,
            "rating": self.rating,
            "regularOpeningHours": self.regularOpeningHours,
            "utcOffsetMinutes": self.utcOffsetMinutes,
            "userRatingCount": self.userRatingCount,
            "currentOpeningHours": self.currentOpeningHours,
            "primaryType": self.primaryType,
            "accessibilityOptions": self.accessibilityOptions
        }

    @staticmethod
    def list_to_dict(places_list):
        return [place.to_dict() for place in places_list]

    @staticmethod
    def from_tuple(data_tuple):
        (displayName, id, types, location, viewport, rating, regularOpeningHours, utcOffsetMinutes, userRatingCount,
         currentOpeningHours, primaryType, accessibilityOptions) = data_tuple

        # Convert string representations of dicts to actual dictionaries if not None
        location = eval(location) if location is not None else None
        viewport = eval(viewport) if viewport is not None else None
        regularOpeningHours = eval(regularOpeningHours) if regularOpeningHours is not None else None
        currentOpeningHours = eval(currentOpeningHours) if currentOpeningHours is not None else None
        accessibilityOptions = eval(accessibilityOptions) if accessibilityOptions is not None else None

        return {
            "id": id,
            "displayName": displayName,
            "types": types,
            "location": location,
            "viewport": viewport,
            "rating": rating,
            "regularOpeningHours": regularOpeningHours,
            "utcOffsetMinutes": utcOffsetMinutes,
            "userRatingCount": userRatingCount,
            "currentOpeningHours": currentOpeningHours,
            "primaryType": primaryType,
            "accessibilityOptions": accessibilityOptions
        }
