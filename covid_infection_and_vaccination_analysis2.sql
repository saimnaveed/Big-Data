--Getting all contents from the CovidVaccination Table(SQL Server)

--select *
--from Analysis..CovidVaccinations

--Joining all contents of Covid Deaths and Covid Vaccination Table

--select * 
--from Analysis..CovidDeaths dt join Analysis..CovidVaccinations vac
--on dt.location=vac.location and dt.date=vac.date

--Getting required data from both table using joins
--select dt.continent,dt.location,dt.date,dt.population,vac.new_vaccinations
--from Analysis..CovidDeaths dt 
--join Analysis..CovidVaccinations vac
--on dt.location=vac.location 
--and dt.date=vac.date
--where dt.continent is not Null
--order by 2,3

--Getting data from both tables(using joins) , partitioned it by location and used CTE(Common Table Expression) for temporary storage and used it for further calculations

--with vacvspop (Continent, Location,Date,Population, New_Vaccinations, Latest_Vaccination_Count)
--as(
--select dt.continent,dt.location,dt.date,dt.population,vac.new_vaccinations , SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (PARTITION BY dt.location order by dt.location,dt.date) as Latest_Vaccination_Count
--from Analysis..CovidDeaths dt 
--join Analysis..CovidVaccinations vac
--	on dt.location=vac.location 
--	and dt.date=vac.date
--where dt.continent is not Null
----order by 2,3
--)
--Select *,(Latest_Vaccination_Count/	Population)*100 as Vaccination_Percentage
--from vacvspop

-- Using Temp Tables for for temporary storage

--Drop Table if exists #VaccinatedPercentage
--create table #VaccinatedPercentage( Continent nvarchar(255), Location nvarchar(255), Date datetime, Population numeric, new_vaccinations numeric, Latest_Vaccination_Count numeric)

--insert into #VaccinatedPercentage

--select dt.continent,dt.location,dt.date,dt.population,vac.new_vaccinations , SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (PARTITION BY dt.location order by dt.location,dt.date) as Latest_Vaccination_Count
--from Analysis..CovidDeaths dt 
--join Analysis..CovidVaccinations vac
--	on dt.location=vac.location 
--	and dt.date=vac.date
--where dt.continent is not Null

--Select * ,(Latest_Vaccination_Count/Population)*100 as Vaccinated_Percentage
--from #VaccinatedPercentage

--Creating Views for visualizations

Create View vaccinations_percentage as
select dt.continent,dt.location,dt.date,dt.population,vac.new_vaccinations , SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (PARTITION BY dt.location order by dt.location,dt.date) as Latest_Vaccination_Count
from Analysis..CovidDeaths dt 
join Analysis..CovidVaccinations vac
	on dt.location=vac.location 
	and dt.date=vac.date
where dt.continent is not Null

--Selecting/Printing the content of the view

select * from [vaccinations_percentage]

--Droping the view
--Drop View vaccinations_percentage 
