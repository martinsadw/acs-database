import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_styles
from database.students import get_students_index
from database.get_data import get_students_styles
from database.process_data import get_distances_matrix

from utils.misc import style_distance


students_db = open_students()
styles_db = open_styles()

students_index = get_students_index(students_db, filter_group=1)

students_styles = get_students_styles(students_index, styles_db)

styles_distances = get_distances_matrix(students_styles, style_distance)

################################################################################

fig = plt.figure()
fig.suptitle('Distância de estilos')
ax = fig.add_subplot(111)
cmap = ax.imshow(styles_distances, interpolation='nearest', origin='lowest', cmap='gray')
plt.show()
