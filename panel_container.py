class SimplePanel:
    MIN_H = 50.0
    def __init__(self, corners_2D, heights):
        self.b_cs = corners_2D
        
        self.hs = []
        for i, c in enumerate(corners_2D):
            self.hs.append(heights[i % len(heights)])

    def get_minimum_height(self):
        smallest_h = SimplePanel.MIN_H
        for h in self.hs:
            if h < smallest_h:
                smallest_h = h

        return smallest_h

    def set_minimum_height(self):
        smallest_h = self.get_minimum_height()
        if smallest_h < SimplePanel.MIN_H:
            h_delta = SimplePanel.MIN_H - smallest_h
            self.hs = [h + h_delta for h in self.hs]

    def get_points(self):
        return [(x, y, self.hs[i]) for i, (x,y) in self.b_cs]

class WithCenterpoin(SimplePanel):
    def __init__(self, corners_2D, heights, centerpoint):
        self.