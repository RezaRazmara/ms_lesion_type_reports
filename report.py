"""
    we have 3 classes here
    - Report (abstract class)
    - ReportString (implemeneted Report)
    - ReportExcel (implemented Report)
    Report is an abstract class that used as interface for other classes like ReportString and ReportExcel
"""
from data_models import Subject, Hemsphere, Lesion
from abc import ABC, abstractmethod
from data_models import lesion_types

class Report(ABC):
    @abstractmethod
    def report(subject: Subject) -> None:
        pass
    
    @abstractmethod
    def _hemsphere_report( hemspehre: Hemsphere):
        pass

    @abstractmethod
    def _lesion_report(lesion: Lesion):
        pass
    
class ReportString(Report):
    def report(subjects: Subject) -> None:
        report = ""
        for subject in subjects:
            report += subject.name +"\n"
            for hemsphere in [subject.left_hemsphere, subject.right_hemsphere]:
                report += subject.name +" "+ReportString._hemsphere_report(hemsphere) +"\n"
        print(report)

    def _hemsphere_report(hemsphere: Hemsphere) -> str:
        report = f"{hemsphere.name} \n"
        for each_lesion_type in hemsphere.lesions.keys():
            report += ReportString._lesion_report(hemsphere.lesions[each_lesion_type])
        return report
    
    def _lesion_report(lesion: Lesion) -> str:
         return f"type: {lesion.type} number: {lesion.number} size: {lesion.size}\n"

class ReportExcel(Report):
    def report(subjects) -> None:
        
        import openpyxl
        import pandas as pd

        # Create a new Excel workbook
        workbook = openpyxl.Workbook()
        # Select the default sheet (usually named 'Sheet')
        sheet = workbook.active
        # Add data to the Excel sheet
        data = [
            ["CODE","left_1", "left_v_1", "left_2", "left_v_2","left_3", "left_v_3","left_4", "left_v_4", "left_5", "left_v_5",
            "right_1", "right_v_1", "right_2", "right_v_2","right_3", "right_v_3","right_4", "right_v_4", "right_5", "right_v_5",
            "all_1", "all_v_1", "all_2", "all_v_2","all_3", "all_v_3","all_4", "all_v_4","all_5", "all_v_5"],
        ]

        for subject in subjects:
            result_subject = [subject.name]
            for hemsphere in [subject.left_hemsphere, subject.right_hemsphere]:
                result_subject.extend(ReportExcel._hemsphere_report(hemsphere))
            result_subject.extend(subject.get_all_lesions())
            print(result_subject)    
            data.append(result_subject)

        for row in data:
            sheet.append(row)

        # Save the workbook to a file
        workbook.save("lesion_statistics.xlsx")
        # Print a success message
        print("Excel file created successfully!")
    
    def _hemsphere_report(hemsphere: Hemsphere) -> list[int]:
        lesion_list = []
        for each_lesion_type in hemsphere.lesions.keys():
            lesion_list.extend(ReportExcel._lesion_report(hemsphere.lesions[each_lesion_type]))
        return lesion_list
    
    def _lesion_report(lesion: Lesion) -> list[int]:
        return [lesion.number, lesion.size]

def report(report: Report, subjects):
    report.report(subjects)
