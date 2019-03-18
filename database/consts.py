from collections import defaultdict

quant_materials_subjects = defaultdict(int, {1: 62, 2: 56, 4: 39, 5: 58, 7: 31, 8: 38})

quant_concepts_subjects = defaultdict(int, {1: 6, 2: 7, 4: 3, 5: 6, 7: 3, 8: 5})

concept_subject = defaultdict(int, {
    1: 1, 3: 1, 5: 1, 38: 1, 39: 1, 40: 1,
    6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2,
    13: 4, 14: 4, 16: 4,
    17: 5, 18: 5, 20: 5, 21: 5, 22: 5, 23: 5,
    24: 7, 25: 7, 26: 7,
    33: 8, 34: 8, 35: 8, 36: 8, 37: 8
})
