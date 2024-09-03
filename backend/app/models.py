# models.py
from sqlalchemy import Column, Integer, String, Float, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class SiteInfo(Base):
    __tablename__ = 'site_info_nad83'
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, comment="Unique identifier for the site")
    state = Column(String(2), nullable=False, comment="Two-letter state code where the site is located")
    agencycd = Column(String, comment="Code of the agency responsible for the site")
    siteno = Column(Float, comment="Site number")
    sitename = Column(String, comment="Name of the site")
    declatva = Column(Float, comment="Decimal latitude of the site")
    declongva = Column(Float, comment="Decimal longitude of the site")
    horzdatum = Column(String, comment="Horizontal datum used for coordinates")
    altva = Column(Float, comment="Altitude value")
    altunits = Column(Integer, comment="Units of altitude measurement")
    welldepth = Column(Float, comment="Depth of the well")
    nataquifercd = Column(String, comment="National aquifer code")
    nataqfrdesc = Column(String, comment="Description of the national aquifer")
    sitetype = Column(String, comment="Type of the site")
    aquifertype = Column(String, comment="Type of aquifer")
    geom = Column(Geometry('POINT', srid=3857), comment="Geographic location of the site")

class Fault(Base):
    __tablename__ = 'usa_all_faults'
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, comment="Unique identifier for the fault")
    fnode_ = Column(Integer, comment="From node")
    tnode_ = Column(Integer, comment="To node")
    lpoly_ = Column(Integer, comment="Left polygon")
    rpoly_ = Column(Integer, comment="Right polygon")
    length = Column(Float, comment="Length of the fault")
    kbf_ = Column(Integer, comment="KBF value")
    kbf_id = Column(Integer, comment="KBF ID")
    desc_ = Column(String, comment="Description")
    ltype = Column(SmallInteger, comment="Line type")
    long_desc = Column(String, comment="Long description")
    alc = Column(SmallInteger, comment="ALC value")
    descltype = Column(String, comment="Description of line type")
    shape_length = Column(Float, comment="Shape length")
    geom = Column(Geometry('GEOMETRY', srid=3857), comment="Geometry of the fault")


class UrbanArea(Base):
    __tablename__ = 'urban_areas'
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    uace10 = Column(String)
    geoid10 = Column(String)
    name10 = Column(String)
    namelsad10 = Column(String)
    lsad10 = Column(String)
    mtfcc10 = Column(String)
    uatyp10 = Column(String)
    funcstat10 = Column(String)
    aland10 = Column(Float)
    awater10 = Column(Float)
    intptlat10 = Column(String)
    intptlon10 = Column(String)
    shape_length = Column(Float)
    shape_area = Column(Float)
    geom = Column(Geometry('GEOMETRY', srid=3857))