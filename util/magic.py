class Magic(object):
    @staticmethod
    def genMountainItems(border, n=10):
        items = []
        (colIdx, rowIdx) = border
        for i in range(n):
            item = MountainItem(Config(**mountainItemConfig))
            item.setPosIndex(random.randint(0, colIdx - 1), random.randint(0, rowIdx - 1))
            items.append(item)

        return items