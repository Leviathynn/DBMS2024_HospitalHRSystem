# DBMS2024_MedicalInsurance
For Database class in Fall 2024. Concept is that of a Medical Insurance calculator and analyzer

CREATE TABLE PATIENT
(
	Patient_ID		VARCHAR(10)	NOT NULL,
    Policy_ID	VARCHAR(10) NOT NULL,
    Fname	VARCHAR(15),
    Lname	VARCHAR(15),
    DOB		DATE,
    Sex		CHAR,
    Blood_Type	VARCHAR(3),
    
    PRIMARY KEY(Patient_ID),
	  FOREIGN KEY(Policy_ID) REFERENCES INSURANCE(Policy_Num)
);

CREATE TABLE INSURANCE
(
	Policy_Num VARCHAR(10) NOT NULL,
    Charges		DEC,
    Provider	VARCHAR (20),
    
    PRIMARY KEY(Policy_Num)
);

CREATE TABLE LIFESTYLE
(
	Case_Num	VARCHAR(10) NOT NULL,
    Age	INT(2),
    BMI	DEC,
    Children	INT(2),
    Smoker	BOOL,
    Region	VARCHAR(20),
    Medical_Conditions VARCHAR(20),
    
    FOREIGN KEY(Case_Num) REFERENCES INSURANCE(Policy_Num)
);
