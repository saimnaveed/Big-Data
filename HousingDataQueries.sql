
--1-Showing All data from the Table HousingData

--select *
--from analysis2..HousingData

--2-Converting the format of SaleDate from datetime to date and updating the table
--Chnaging the datatype of the column is done by using 'alter' keyword as it is a DDL operation not DML operation so can't be performed by using update keyword

--select SaleDate,convert(Date,SaleDate)
--from analysis2..HousingData

--alter table analysis2.dbo.HousingData
--Alter column SaleDate Date;

--3-Getting the columns having Null value in PropertyAddress from the table in a particular order

--select *
--from analysis2..HousingData
--where PropertyAddress is NULL
--order by ParcelID

--Filling the Null values for the field of property address using joins
--First we have checked that can we fill the Null values in  the field of PropertyAddress & for this we have used self join and isnull() function

--select a.UniqueID, a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress,ISNULL(a.PropertyAddress,b.PropertyAddress)
--from analysis2..HousingData a join analysis2..HousingData b
--on a.ParcelID=b.ParcelID and a.UniqueID != b.UniqueID
--where a.PropertyAddress is NULL

--In this second step we have updated the Null values in the field of PropertyAddress with the property address of those entries who have same ParcelID as it has

--Update a
--set a.PropertyAddress=ISNULL(a.PropertyAddress,b.PropertyAddress)
--from analysis2..HousingData a join analysis2..HousingData b
--on a.ParcelID=b.ParcelID and a.UniqueID != b.UniqueID
--where a.PropertyAddress is NULL

--4- Breaking the Address Column into Multiple Coulmns and update the table


-- Splitting the PropertyAddress into propertyAddress and PropertyCity
--used for chceking/testing the workability of the solution

--select 
--substring(PropertyAddress,1,charindex(',',PropertyAddress)-1) as Street_Address,
--substring(PropertyAddress,charindex(',',PropertyAddress)+1,len(PropertyAddress)) as City_Address
--from analysis2..HousingData

-- Adding the new columns in the table and put in the desired values

--Alter table analysis2..HousingData
--Add PropertyAddressSplitted Nvarchar(255), PropertyCitySplitted Nvarchar (255)

--update analysis2..HousingData
--set PropertyAddressSplitted = substring(PropertyAddress,1,charindex(',',PropertyAddress)-1)
--update analysis2..HousingData
--set PropertyCitySplitted = substring(PropertyAddress,charindex(',',PropertyAddress)+1,len(PropertyAddress))

--5- Splitting the OwnersAddress into Street, City adn State Columns
--Creating the New Columns
--Alter table analysis2..HousingData
--Add OwnerAddressSplitted Nvarchar(255), OwnerCitySplitted Nvarchar (255), OwnerStateSplitted Nvarchar (255)

--Adding values to the new columns

--update analysis2..HousingData
--set OwnerAddressSplitted = parsename(replace(OwnerAddress,',','.'),3)
--update analysis2..HousingData
--set OwnerCitySplitted = parsename(replace(OwnerAddress,',','.'),2)
--update analysis2..HousingData
--set OwnerStateSplitted = parsename(replace(OwnerAddress,',','.'),1)

--6- Setting the values in the column SoladasVacant to a Standard Format Yes or No

--update analysis2..HousingData
--set SoldAsVacant= CASE when SoldAsVacant ='Y' then 'Yes'
--when SoldAsVacant ='N' then 'No'
--Else SoldAsVacant
--End

--select SoldAsVacant
--  from analysis2..HousingData

--7-Removing Duplicates
--Making a cte using window functions and assigning numbers to each row  to check if underlined column values are same in multiple rows

--with rownumcte as(
--Select *,
--	 ROW_NUMBER() over(partition by ParcelID, PropertyAddress, SalePrice, SaleDate, LegalReference Order by UniqueID) row_num
--From analysis2..HousingData)
 
----For checking the presence of duplicates
--Select *
--from rownumcte
--where row_num >1

---- Removing the duplicate values
--Delete
--from rownumcte
--where row_num >1

--8- Making a view to get the customized version of the sql table
-- Removing Unused or irrelevant coulmns from it

--create view efficientdataview as 
--select *
--from analysis2..HousingData

--Select *
--from efficientdataview

--alter view efficientdataview as
--select UniqueID, ParcelID,LandUse,SalePrice,LegalReference,SoldAsVacant,OwnerName,Acreage,LandValue,BuildingValue,TotalValue,YearBuilt,Bedrooms,FullBath,HalfBath,PropertyAddressSplitted,PropertyCitySplitted,OwnerAddressSplitted,OwnerCitySplitted,OwnerStateSplitted
--from analysis2..HousingData

--This can be done by removing columns from the original table which is not advisable

--Alter table
--drop column PropertyAddres,TaxDistrict, OwnerAddress