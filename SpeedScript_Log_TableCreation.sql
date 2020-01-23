BEGIN TRANSACTION
SET QUOTED_IDENTIFIER ON
SET ARITHABORT ON
SET NUMERIC_ROUNDABORT OFF
SET CONCAT_NULL_YIELDS_NULL ON
SET ANSI_NULLS ON
SET ANSI_PADDING ON
SET ANSI_WARNINGS ON
COMMIT
BEGIN TRANSACTION
GO
CREATE TABLE [dbo].[SpeedScript_Log]
	(
	lastName varchar(10) NULL,
	firstName varchar(20) NULL,
	stateID varchar(20) NOT NULL,
	grade varchar(5) NULL,
	schoolName nvarchar(30) NULL,
	startYear smallint NULL,
	endYear smallint NULL,
	courseNumber varchar(13) NOT NULL,
	courseName varchar(60) NULL,
	stateCode varchar(20) NULL,
	score varchar(10) NULL,
	actualTerm tinyint NULL,
	startTerm tinyint NULL,
	endTerm tinyint NULL,
	termsLong tinyint NULL,
	gpaWeight decimal(6,3) NULL,
	gpaMax decimal(7,4) NULL,
	creditsEarned decimal(6,3) NULL,
	creditsAttempted decimal(6,3) NULL,
	creditName varchar(20) NOT NULL,
	termStartDate smalldatetime NULL,
	termEndDate smalldatetime NULL,
	distanceCode varchar(5) NULL,
	specialGPA bit NULL,
	summerSchool bit NULL

	)  ON [PRIMARY]
GO
ALTER TABLE [dbo].[SpeedScript_Log] SET (LOCK_ESCALATION = TABLE)
GO
COMMIT