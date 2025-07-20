-- Getting all contents of Covid Vaccination Table through (SQL Server)

Select *
From dbo.CovidVaccinations
order by 3,4

-- Getting all contents of Covid Deaths Table

Select *
From dbo.CovidDeaths
order by 3,4

-- Getting desired content in an order from Covid Deaths

Select location, date, total_cases, new_cases, total_deaths, population
From Analysis..CovidDeaths
order by 1,2

-- Getting country wise death percentage

Select location, SUM(CAST(new_cases as int)) as Total_Cases, SUM(CAST(new_deaths as int)) as Total_Deaths,(SUM(CAST(new_deaths as float))/SUM(CAST(new_cases as float)))*100 as Death_Percentage
From Analysis..CovidDeaths
group by location
order by location

-- Getting death rate change with time w.r.t covid cases

Select location,date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Death_Rate
From Analysis..CovidDeaths
where location like '%state%'
order by 1,2

--Percentage of Covid Cases w.r.t population/ infection Rates

Select location,date, total_cases, total_deaths, (total_cases/population)*100 as Covid_Patients_Percentage
From Analysis..CovidDeaths
--where location like '%state%'
order by 1,2

-- Getting Highest percentage of Covid Infection w.r.t Every Country
Select location, population, max(total_cases) as Highest_Cases, (max(total_cases/population))*100 as Highest_Disease_Rate
From Analysis..CovidDeaths
group by location,population
order by Highest_Disease_Rate Desc

--Getting Highest Death Count by country
select location, population, max(cast(total_deaths as int)) as Death_Count, (max(cast(total_deaths as int))/max(total_cases))*100 as Death_Rate
from Analysis..CovidDeaths
where continent is not Null
group by location, population
order by Death_Count desc;

select location, max(cast(total_deaths as int)) as Death_Count, (max(cast(total_deaths as int))/max(total_cases))*100 as Death_Rate
from Analysis..CovidDeaths
where continent is  Null
group by location
order by Death_Count desc;

--Getting Highest Death Count w.r.t Continent
select continent, max(cast(total_deaths as int)) as Death_Count, (max(cast(total_deaths as int))/max(total_cases))*100 as Death_Rate
from Analysis..CovidDeaths
where continent is  not Null
group by continent
order by Death_Count desc;

--Statistics per day all over the world

select sum(new_cases) as Covid_Cases,sum(cast(new_deaths as int)) as Death_Count,(sum(cast(new_deaths as int))/sum(new_cases))*100 as Death_Percentage
from Analysis..CovidDeaths
where continent is not Null

select date,sum(new_cases) as Covid_Cases,sum(cast(new_deaths as int)) as Death_Count,(sum(cast(new_deaths as int))/sum(new_cases))*100 as Death_Percentage
from Analysis..CovidDeaths
where continent is not Null
group by date
order by date
