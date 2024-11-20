"""
we have 3 classes here:
    - Subject
    - Hemsphere
    - Lesion

description:
    each Subject for our study has two Hemspheres in the brain and in each
    hemsphere we have some Lesions produced by MS disease. 

"""

import nibabel as nib
import numpy as np
from scipy import ndimage
from abc import ABC, abstractmethod

# we have 5 types of lesion detected in MS disease
lesion_types = [1, 2, 3, 4, 5]

class Lesion:
    """
        each lesion in MS disease has a type the show the status of progression of desease,
    """
    def __init__(self, type: str, number: int,  size: int):
        self.type = type
        self.number = number
        self.size = size 

    def add_number(self):
        """
            new lesion found for this type
        """
        self.number +=  +1

    def add_size(self, size):
        """
            update lesion size of this type.
        """
        self.size += size
class Hemsphere:
    """
        Hemsphere is half of the brain and it could be left or right
    """
    def __init__(self, name ,hemsphere_label_map):
        
        # name of the hemsphere : left or right
        self.name = name
        
        # labeled map of each hemsphere
        self.hemsphere_label_map = hemsphere_label_map

        # for each lesion type we have a seprate key 
        self.lesions = {
            1: Lesion("1",0,0),
            2: Lesion("2",0,0),
            3: Lesion("3",0,0),
            4: Lesion("4",0,0),
            5: Lesion("5",0,0)
        }

        self._analyse_each_lesion()

    def _add_new_lesion(self, each_lesion) -> None:
        """
            update lesions dictionary based on each new lesion we analyzed.
        """
        lesion_type = each_lesion % 100
        lesion_size = len(self.hemsphere_label_map[self.hemsphere_label_map == each_lesion])
        
        self.lesions[lesion_type].add_number()
        self.lesions[lesion_type].add_size(lesion_size)
    

    def _analyse_each_lesion(self) -> None:
        """
            for each labeld lesion we analysis it to know which type it is.
            then we update the lesions dictionary based on our findings.
        """
        hemsphere_label_map_uniques = np.unique(self.hemsphere_label_map)[1:]
        
        for each_lesion in hemsphere_label_map_uniques:
            self._add_new_lesion(each_lesion)



class Subject:
    """
        each subject has two left and right hemspheres in the brain 
    """ 
    def __init__(self, name, file_address):
        self.name = name

        self.left_hemsphere, self.right_hemsphere = self._get_left_and_right_hemspheres(file_address=file_address) 
        left_label_map, unique_label, count_label = self._clustering_lesions(self.left_hemsphere)
        right_label_map, unique_label, count_label = self._clustering_lesions(self.right_hemsphere)

        self.left_label_map = left_label_map * 100 + self.left_hemsphere
        self.right_label_map = right_label_map * 100 + self.right_hemsphere

        self.left_hemsphere = Hemsphere("left", self.left_label_map)
        self.right_hemsphere = Hemsphere("right", self.right_label_map)


    def _get_left_and_right_hemspheres(self, file_address) -> tuple[Hemsphere]:
        """
            split the brain mri image to two seprate matrixes to represent each hemsphere of the brain
        """
        img_proxy = nib.load(file_address)
        img_data = img_proxy.get_fdata()

        left_hemsphere = img_data[: (img_data.shape[0]//2), :, :]
        right_hemsphere = img_data[(img_data.shape[0]//2) :, :, :]

        return left_hemsphere, right_hemsphere
    
    def _clustering_lesions(self,hemsphere, struct=np.ones([3,3,3])) -> tuple:
        """
            cluster each lesion in each hemsphere to count them and to label them
        """
        label_map,num_features = ndimage.label(hemsphere,structure=struct)
        unique_label, count_label = np.unique(label_map,return_counts=True)
        return label_map, unique_label, count_label

    def get_all_lesions(self) -> list[int]:
        """
            each lesion has a different type and it could be one of 1, 2, 3, 4, 5,
            we want to know and count the number of each type and the whole size of each type
        """
        result = []
        for lesion_type in lesion_types:
            left_hemsphere_lesion_type = self.left_hemsphere.lesions[lesion_type]
            right_hemsphere_lesion_type = self.right_hemsphere.lesions[lesion_type]
            result.extend([left_hemsphere_lesion_type.number + right_hemsphere_lesion_type.number, 
                           left_hemsphere_lesion_type.size + right_hemsphere_lesion_type.size])
        return result
    
