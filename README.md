# Separating-Axis-Theorem
Using Separating Axis Theorem to detect if 2 objects are intersecting in pygame


So, using the logic of Separating Axis Theorem that if you cant draw a line in between 2 squares then they are overlapping and colliding. I made something close, its not perfect but its close, I also haven't accounted for rotation of squares but if you find a way to find the vertices/corners of the square, then this could easily work. The way i did it was that i turned the squares into lines and drew a line directly in the middle of the squares and at the normal of the line in between the squares, its a bit confusing but it makes sense once you see it. I then used [line intersecting maths](https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Intersection_of_two_lines) to find if they intersect.

doing rotating squares: added rotation variable in square class, i used [this](https://gamedev.stackexchange.com/questions/86755/how-to-calculate-corner-positions-marks-of-a-rotated-tilted-rectangle/86784#86784) answer to find the corners of the square, then once i have the corners, used the line intersetion.
