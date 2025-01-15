create table RequestActivityStatus
(
[Id] [int] primary key  IDENTITY(1,1) NOT NULL,
	[NameEn] [varchar](350) NOT NULL,
	[NameFa] [nvarchar](400) NULL,
	Daily bit default 1,
	UserInvisible bit default 0
)

create table ProcessStatus
(
[Id] [int] primary key  IDENTITY(1,1) NOT NULL,
	[NameEn] [varchar](100) NOT NULL,
	[NameFa] [nvarchar](200) NULL,
)

create table UserRequestActivity
(
[Id] [int] primary key IDENTITY(1,1) NOT NULL,
[UserId] [int] NOT NULL,
constraint fk_UserRequestActivity_RequesterUserId
foreign key ([UserId])
references Users(Id),
[ProcessStatusId] int NOT NULL,
constraint fk_UserRequestActivity_processId
foreign key ([ProcessStatusId])
references ProcessStatus(Id),
Reason nvarchar(300) null,
Description nvarchar(max) null,
Date date not null,
ToDate date,
FromTime time,
ToTime time,
[DateCreated] [datetime] NOT NULL,
[DateUpdated] [datetime],
[ConfirmerUserId] int,
constraint fk_ConfirmerUserId_UserRequestActivity
foreign key ([ConfirmerUserId])
references Users(Id),
[RequestActivityStatusId] [int] not NULL,
	constraint fk_UserRequestActivity_RequestActivityStatusId
	foreign key ([RequestActivityStatusId])
	references RequestActivityStatus(Id),
[AdminUserId] int NULL,
constraint fk_AdminActionUserId_RequestShiftSwap
foreign key ([AdminUserId])
references Users(Id),
[AdminActionDate] [datetime] NULL
	
)



create table UserRequestShiftChange(
	[Id] [int] primary key IDENTITY(1,1) NOT NULL,
	[ShiftDate] [date] NOT NULL,
	[ProcessStatusId] int NOT NULL,
	constraint fk_UserShiftSwapEvent_processId
	foreign key ([ProcessStatusId])
	references ProcessStatus(Id),
	[RequesterUserId] [int] NOT NULL,
	constraint fk_RequesterUserId_RequestShiftSwap
	foreign key ([RequesterUserId])
	references Users(Id),
	[ReceiverUserId] [int] NULL,
	constraint fk_ReceiverUserId_RequestShiftSwap
	foreign key ([ReceiverUserId])
	references Users(Id),
	[RequesterShiftTimeStatusId] int NOT NULL,
	constraint fk_RequesterShiftTimeId
	foreign key ([RequesterShiftTimeStatusId])
	references ShiftTimeStatus(Id),
	[ReceiverShiftTimeStatusId] int NOT NULL,
	constraint fk_ReceiverShiftTimeId
	foreign key ([ReceiverShiftTimeStatusId])
	references ShiftTimeStatus(Id),
	[RequesterShiftStatusId] int NOT NULL,
	constraint fk_RequesterShiftStatusId_StatusId
	foreign key ([RequesterShiftStatusId])
	references ShiftStatus(Id),
	[ReceiverShiftStatusId] int NOT NULL,
	constraint fk_ReceiverShiftStatusId
	foreign key ([ReceiverShiftStatusId])
	references ShiftStatus(Id),
	[RequesterActionDate] [datetime] NULL,
	[ReceiverActionDate] [datetime] NULL,
	[PilotId] [int] NULL,
	constraint fk_UserShiftSwapEvent_pilotId
	foreign key ([PilotId])
	references Pilots(Id),
	[PilotFlagId] [int] NULL,
	constraint fk_UserShiftSwapEvent_pilotflagid
	foreign key ([PilotFlagId])
	references Pilotflag(Id),
	[AdminUserId] int NULL,
	constraint fk_AdminActionUserId_UserRequestShiftChange
	foreign key ([AdminUserId])
	references Users(Id),
	[AdminActionDate] [datetime] NULL,
	[MultipleCode] [varchar](max) NULL,
	
)
