"""
    starting point of project.
    - it gets the address of mri images of brain, its classified lesions detected by doctors specialized in MS disease,
        doctors classified each lesion as one of five types [1,2,3,4,5].

    - the output is the report of each lesion type: the number of each type and the size of each type. 
"""

from file_reader import FileReader
from report import ReportString, ReportExcel, report

if __name__ == "__main__":
    """
        in the folder the name of files are as follows:
            - qsm_sub1_RR_CL.nii.gz
            - qsm_sub2_RR_CL.nii.gz
            - qsm_sub3_RR_CL.nii.gz
            - ...
    """
    folder_address = "C:\\Users\\Reza\\Desktop\\final_projects\\Classified_QSM_classification_RR\\"
    list_of_subjects = FileReader.get_list_of_subjects(folder_address)
    
    #report(ReportString, list_of_subjects)
    report(ReportExcel, list_of_subjects)