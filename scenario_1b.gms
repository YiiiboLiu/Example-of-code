Sets
         t               time
                 / 1*8760        all hours of the year /


         storage            storage used in system
                 / battery
                   hydrogen
                   heat
                    /

         storageprop       plant properties
                 /es_investment    annulized energy storage capacity investment cost [EUR per kWh]
                  in_investment    annulized input capacity investment cost [EUR per kW]
                  out_investment   annulized output capacity investment cost [EUR per kW]
                  om_cost          O&M cost [EUR per MWh]
                  ch_efficiency    Charge efficiency
                  dis_efficiency   Discharge efficiency/

         m                  microgrid a&b
                 /a      microgrid a
                  b      microgrid b/
;

Parameters
******** Input data to read from files
         p_load_ind(t)               electricity demand profile of Lepa [kW  hour]
         p_load_com(t)               electricity demand profile of Uttag [kW \ hour]
         p_wind(t)                   normalized wind production profile [kW \ hour]
         p_hydro(t)                  normalized wind production profile [kW \ hour]
         p_networktariff_ind(t)      network tariff for ebought in Lepa [kr \ kWh]
         p_networktariff_com(t)      network tariff for ebought in Uttag [kr \ kWh]


******** Model settings
         p_cableinv              Annualized investment costs of cable [Euro \(kW*km)\year]
         p_main2grid_caa         Transformer power capacity between microgrid a and main grid [kw]
         p_main2grid_cab         Transformer power capacity between microgrid b and main grid [kw]
         p_cable_l               Length of cable investment [km]


******** Parameters that will be calculated later


* Read load profile from file 'demand_Lepa.inc'
Parameter p_load_ind(t) /
$include ./inc/demand_Lepa_100.inc
/;

* Read load profile from file 'demand_Uttag.inc'
Parameter p_load_com(t) /
$include ./inc/demand_Uttag_100.inc
/;

* Read wind profile from file 'wind.inc'
Parameter p_wind(t) /
$include ./inc/wind.inc
/;

* Read wind profile from file 'hydro.inc'
Parameter p_hydro(t) /
$include ./inc/hydro.inc
/;

* Read electricity price profile from file 'eprice2018.inc'
Parameter p_eprice(t) /
$include ./inc/eprice2018.inc
/;

* Read network tariff profile from file 'networktariff_ind.inc'
Parameter p_networktariff_ind(t) /
$include ./inc/networktariff_ind.inc
/;

* Read network tariff profile from file 'networktariff_com.inc'
Parameter p_networktariff_com(t) /
$include ./inc/networktariff_com.inc
/;

Table p_storageprop(storageprop,storage)       table of storage properties[Euro\kWh]
                 battery       hydrogen  heat
es_investment    83.61         4.044     4.08
in_investment    0.54          55.875    0
out_investment   0.54          78.089    119.15
ch_efficiency    0.98          0.66      1
dis_efficiency   0.97          0.53      0.275
om_cost          0.002         0         0
;

*Annualized investment costs of cable [Euro \(kW*km)\year]
p_cableinv =3.2866;

*Transformer power capacity between microgrid a and main grid [kw]
p_main2grid_caa = 60000;

*Transformer power capacity between microgrid b and main grid [kw]
p_main2grid_cab = 36000;

*Length of cable investment [km]
p_cable_l=2;
*------------------------------------------------------------------------------------------------------------
*REMOVE examples and add your own variables,positive variables and equations.

* Free variables that can be both positive and negative (variable to be minimized must be free)
Variables
         v_tra(m,t)                    Electricity transmitted from microgrid m to another microgrid  at time t [kWh]
         v_total_cost                    Total system cost [Euro]
;
* Positive variables
Positive variables
         v_total_energycapinv(m)         Total energy storage capacity investment cost[Euro]
         v_total_inputcapinv(m)          Total input capacity investment cost[Euro]
         v_total_outputcapinv(m)         Total output capacity investment cost[Euro]
         v_total_var(m)                  Total variable cost[Euro]
         v_totalprice(m)                 Total cost of importing electricity from main grid [Euro]
         v_totalsellprice(m)             Total cost of exporting electricity from main grid [Euro]
         v_totalnetworkbought(m)         Total network tariff of importing electricity from main grid [Euro]
         v_totalnetworksell              Total network tariff of exporting electricity from main grid [Euro]
         v_cablecost                     Total cost of cable investment[Euro]
         v_energycap(m,storage)          Energy storage capacity investment in technology i connected to microgrid m [kWh]
         v_incap(m,storage)              Input capacity investment in technology i connected to microgrid m [kW]
         v_outcap(m,storage)             Output capacity investment in technology i connected to microgrid m [kW]
         v_cablecap                      Cable power capacity investment [kW]
         v_charge(m,storage,t)           Electricity charged by microgrid m to technology i at time t [kWh]
         v_discharge(m,storage,t)        Electricity discharged by technology i to microgrid m at time t [kWh]
         v_storagelevel(m,storage,t)     Storage level in device i connected to microgrid m at time t [kWh]
         v_ebought(m,t)                  Electricity purchased by microgrid m from main grid at time t [kWh]
         v_maxoutput(m,storage,t)        Electricity purchased by microgrid m from main grid at time t [kWh]
         v_esell(m,t)                    Electricity sold by microgrid m[kWh]




;
* Define constraints (inequalities are also termed equations in GAMS)
Equations
         equ_total_energy_inv(m)
         equ_total_inputcapinv(m)
         equ_total_outputcapinv(m)
         equ_total_var(m)
         equ_price(m)
         equ_networkbought_a
         equ_networkbought_b
         equ_cable
         equ_total_sell(m)
         equ_totalnetworksell
         equ_total_cost



         equ_load_a(t)
         equ_load_b(t)
         equ_maxoutput1(m,storage,t)
         equ_maxoutput2(m,storage,t)
         equ_storagelevel(m,storage,t)
         equ_storagelim(m,storage,t)
         equ_storagelimin(m,storage,t)
         equ_storagelimout(m,storage,t)
         equ_boughtlima(t)
         equ_boughtlimb(t)
         equ_selllima(t)
         equ_selllimb(t)
         equ_transmission(t)
         equ_transmissionlim1(m,t)
         equ_transmissionlim2(m,t)
         equ_nminus1_a(t)
         equ_nminus1_b(t)

         equ_tran0(m,t)

;
*=G= for greater than, =L= less than, =E= strict equal to
equ_total_energy_inv(m)..
         v_total_energycapinv(m) =E= sum(storage,v_energycap(m,storage)*p_storageprop('es_investment',storage));
equ_total_inputcapinv(m)..
         v_total_inputcapinv(m) =E= sum(storage,v_incap(m,storage)*p_storageprop('in_investment',storage));
equ_total_outputcapinv(m)..
         v_total_outputcapinv(m) =E= sum(storage,v_outcap(m,storage)*p_storageprop('out_investment',storage));
equ_total_var(m)..
         v_total_var(m) =E= sum(storage,sum(t,v_discharge(m,storage,t)*p_storageprop('om_cost',storage)));
equ_price(m)..
         v_totalprice(m) =E= sum(t,p_eprice(t)*v_ebought(m,t));
equ_networkbought_a..
         v_totalnetworkbought('a') =E= sum(t,p_networktariff_ind(t)*v_ebought('a',t));
equ_networkbought_b..
         v_totalnetworkbought('b') =E= sum(t,p_networktariff_com(t)*v_ebought('b',t));
equ_cable..
         v_cablecost =E= p_cable_l*v_cablecap*p_cableinv;
equ_total_sell(m)..
         v_totalsellprice(m) =E= sum(t,p_eprice(t)*v_esell(m,t));
equ_totalnetworksell..
         v_totalnetworksell =E= sum(t,v_esell('a',t)*0.0023 + v_esell('b',t)*0.009);
equ_total_cost..
         v_total_cost =E= sum(m,v_total_energycapinv(m)) + sum(m,v_total_inputcapinv(m)) + sum(m,v_total_outputcapinv(m)) + sum(m,v_total_var(m)) + sum(m,v_totalprice(m)) -sum(m,v_totalsellprice(m))+ v_cablecost+ sum(m,v_totalnetworkbought(m))-v_totalnetworksell;

equ_load_a(t)..
         p_hydro(t)+v_ebought('a',t)-v_esell('a',t)+sum(storage,v_discharge('a',storage,t)*p_storageprop('dis_efficiency',storage))=G= p_load_ind(t)+sum(storage,v_charge('a',storage,t))+v_tra('a',t);
equ_load_b(t)..
         p_wind(t)+v_ebought('b',t)-v_esell('b',t)+sum(storage,v_discharge('b',storage,t)*p_storageprop('dis_efficiency',storage))=G= p_load_com(t)+sum(storage,v_charge('b',storage,t))+v_tra('b',t);
equ_storagelevel(m,storage,t)..
         v_storagelevel(m,storage,t)=E=v_storagelevel(m,storage,t--1)+v_charge(m,storage,t)*p_storageprop('ch_efficiency',storage)-v_discharge(m,storage,t);
equ_storagelim(m,storage,t)..
         v_storagelevel(m,storage,t)=L=v_energycap(m,storage);
equ_storagelimin(m,storage,t)..
         v_charge(m,storage,t)*p_storageprop('ch_efficiency',storage)=L= v_incap(m,storage);
equ_storagelimout(m,storage,t)..
         v_discharge(m,storage,t)=L=v_outcap(m,storage);

equ_boughtlima(t)..
         v_ebought('a',t)=L=p_main2grid_caa- p_hydro(t);
equ_boughtlimb(t)..
         v_ebought('b',t)=L=p_main2grid_cab;
equ_selllima(t)..
         v_esell('a',t)=L= p_main2grid_caa- p_hydro(t);
equ_selllimb(t)..
         v_esell('b',t)=L= p_main2grid_cab;


equ_transmission(t)..
         v_tra('a',t)=E= 0-v_tra('b',t);
equ_transmissionlim1(m,t)..
         v_tra(m,t)=G=0-v_cablecap;
equ_transmissionlim2(m,t)..
         v_tra(m,t)=L=v_cablecap;
equ_tran0(m,t)..
         v_tra(m,t)=E=0 ;

equ_maxoutput1(m,storage,t)..
         v_maxoutput(m,storage,t)=L= v_storagelevel(m,storage,t)*p_storageprop('dis_efficiency',storage);
equ_maxoutput2(m,storage,t)..
         v_maxoutput(m,storage,t)=L= v_outcap(m,storage);
equ_nminus1_a(t)..
         30000 + sum(storage,v_maxoutput('a',storage,t)) =G= p_load_ind(t);
equ_nminus1_b(t)..
         16000 + p_wind(t) + sum(storage,v_maxoutput('b',storage,t)) =G= p_load_com(t);





* Create model from all equations and solve
*------------------------------------------------------------------------------------------------------------------
Model esmp / all /;
Solve esmp using lp minimizing v_total_cost;

* Write everything to gdx and then selected values to Excel
Execute_unload 'esmp_out.gdx';
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_total_cost rng=v_total_cost!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_total_energycapinv rng=v_total_energycapinv!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_total_inputcapinv rng=v_total_inputcapinv!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_total_outputcapinv rng=v_total_outputcapinv!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_total_var rng=v_total_var!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_cablecost rng=v_cablecost!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_totalprice rng=v_totalprice!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_totalsellprice rng=v_totalsellprice!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_totalnetworkbought rng=v_totalnetworkbought!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_totalnetworksell rng=v_totalnetworksell!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_energycap rng=v_energycap!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_storagelevel  rng=v_storagelevel!a1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_incap  rng=v_incap!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_outcap  rng=v_outcap!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_ebought  rng=v_ebought!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_esell  rng=v_esell!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_cablecap  rng=v_cablecap!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_tra  rng=v_tra!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_charge  rng=v_charge!a1 rdim=1";
execute "gdxxrw esmp_out.gdx o=a_result.xlsx squeeze=0 var=v_discharge  rng=v_discharge!a1 rdim=1";
