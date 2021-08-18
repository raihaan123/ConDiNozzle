%Version 1.1 Copyright William Devenport, Virginia Tech, 1/26/18
function CDN ()
global ui flow;
close all

% Initial states
flow.g=1.4;     % Gamma (Cp/Cv)
flow.xmax=10;   % Max x for nozzle
flow.aeat=2.5;  % Exit / Throat area ratio
flow.pbpc=1;    % Back  / Chamber pressure ratio

% Creating Figure inside UI object
ui.Figure=figure('Units','normalized','Name','Converging-Diverging Nozzle','NumberTitle','off');
set(gcf,'Position',[0.25 0.25 0.40 0.5]);

% Creating axes for each of the three plots
ui.axes(1)=axes('Position',[0.1300    0.7093    0.6    0.2157],'Box','on');
ui.axes(2)=axes('Position',[0.1300    0.4096    0.6    0.2157],'Box','on');
ui.axes(3)=axes('Position',[0.1300    0.1100    0.6    0.2157],'Box','on');
ui.xlim=[-3 12];

% Buttons for preset states
ui.design=uicontrol(gcf,'Style','pushbutton','Units','normalized','Position',[0.77 0.12 0.2 0.05],'String','Design','Callback',@design);
ui.choked=uicontrol(gcf,'Style','pushbutton','Units','normalized','Position',[0.77 0.26 0.2 0.05],'String','Subsonic choked','Callback',@choked);
ui.shockExit=uicontrol(gcf,'Style','pushbutton','Units','normalized','Position',[0.77 0.19 0.2 0.05],'String','Shock at exit','Callback',@shockExit);

% Titles for each slider
ui.pbpcL=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.775 0.90 0.06 0.05],'String','Pb/Pc','FontAngle','italic','FontSize',10);
ui.aeatL=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.84 0.90 0.06 0.05],'String','Ae/At','FontAngle','italic','FontSize',10);
ui.gammaL=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.905 0.90 0.06 0.05],'String','Cp/Cv','FontAngle','italic','FontSize',10);

% Values under each slider
ui.pbpcV=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.775 0.36 0.06 0.03],'String',num2str(flow.pbpc),'FontAngle','italic','FontSize',10);
ui.aeatV=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.84 0.36 0.06 0.03],'String',num2str(flow.aeat),'FontAngle','italic','FontSize',10);
ui.gammaV=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.905 0.36 0.06 0.03],'String',num2str(flow.g),'FontAngle','italic','FontSize',10);

% Actual slider elements
ui.pbpc=uicontrol(gcf,'Style','slider','Units','normalized','Position',[0.785 0.4 0.04 0.52],'Min',0.005,'Max',1,'SliderStep',[0.005 0.1]/0.995,'value',flow.pbpc,'Callback',@pbpcApply);
ui.aeat=uicontrol(gcf,'Style','slider','Units','normalized','Position',[0.85 0.4 0.04 0.52],'Min',1.05,'Max',10,'SliderStep',[0.05 1]/(10-1.05),'Value',flow.aeat,'Callback',@aeatApply);
ui.gamma=uicontrol(gcf,'Style','slider','Units','normalized','Position',[0.915 0.4 0.04 0.52],'Min',1.2,'Max',1.7,'SliderStep',[0.01 0.1]/(1.7-1.2),'Value',flow.g,'Callback',@gammaApply);

% State variable - title block
ui.state=uicontrol(gcf,'Style','text','Units','normalized','Position',[0.28 0.93 0.3 0.05],'Fontsize',12);
flowplot();
end

function flowplot ()
global ui flow;

% Load nozzle + flow parameters
g=flow.g;
aeat=flow.aeat;
xmax=flow.xmax;
pbpc=flow.pbpc;

% Nozzle shape
xc=-3:.1:0;
yc=1+xc.^2/4.5;
xd=0:.1:xmax;
yd=tanh(2*xd/xmax)/tanh(2)*(aeat-1)+1;
x=[xc xd]; y=[yc yd];

%Design exit Mach and pressure
meD=m_aas(aeat,g,1);
pbpcD=pp0(meD,g);flow.pbpcD=pbpcD;

%Subsonic choked exit Mach and pressure
meC=m_aas(aeat,g,0);
pbpcC=pp0(meC,g);flow.pbpcC=pbpcC;

%Shock at exit pressure ratio
pbpcS=p2p1(meD,g)*pbpcD;flow.pbpcS=pbpcS;

axes(ui.axes(1)); % plot nozzle
ymax=max([3 y(end)*1.5]);
fill([x x(end) x(1)],[y  ymax ymax],[0.85 0.85 0.85]);hold on
plot(x,y,'k');ylim([0 ymax]);ylabel('A/A_t');xlim(ui.xlim);
plot([x(end) x(end)],[y(end) ymax],'k');hold off;

if pbpc>=pbpcC %subsonic
    mexit=m_pp0(pbpc,g);
    aeas=aas(mexit,g);
    m=m_aas(y*aeas/aeat,g,0);m(find(y*aeas/aeat<=1))=1;
    ppc=pp0(m,g);
    axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;
    if pbpc<1
        axes(ui.axes(1));hold on; %plot flow
        hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        hold off 
        set(ui.state,'String','Subsonic Flow');
    else
        set(ui.state,'String','No Flow');
    end
elseif pbpc<=pbpcS %over/underexpanded and design
    up=find(x<0);dn=find(x>=0);
    m=[m_aas(y(up),g,0) m_aas(y(dn),g,1)];
    ppc=pp0(m,g);
    axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;
    if pbpc>pbpcD & pbpc<pbpcS
        set(ui.state,'String','Overexpanded Flow');
        xi=pbpc/pp0(m(end),g);m1=m(end);
        beta=asin(sqrt(((g+1)*xi+(g-1))/2/g/m1^2));
        delta=atan(sqrt(((xi-1)/(g*m1^2-xi+1))^2*(2*g*m1^2-(g-1)-(g+1)*xi)/((g+1)*xi+(g-1))));
        axes(ui.axes(1));hold on; %plot flow and shock
        hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end)-(ui.xlim(2)-x(end))*tan(delta) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        xs=[x(end) x(end)+y(end)/2*cot(beta) x(end)+y(end)*cot(beta)];ys=[y(end) y(end)/2 0];m1=meD*sin(beta);
        hshock=plot(xs(1:2),ys(1:2),'r',xs(2:3),ys(2:3),'r:');set(hshock,'linewidth',m1,'color',[0.85 0.85-0.85*tanh(m1-1) 1-tanh(m1-1)]);
        hold off
    elseif pbpc==pbpcD
        set(ui.state,'String','Design Condition');
        axes(ui.axes(1));hold on; %plot flow
        hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        hold off 
    elseif pbpc<pbpcD
        set(ui.state,'String','Underexpanded Flow');
        m1=meD;m2=m_pp0(pbpc,g);theta=nu(m2,g)-nu(m1,g);mu1=asin(1/m1);mu2=asin(1/m2)-theta;
        axes(ui.axes(1));hold on; %plot flow and waves
        hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end)+(ui.xlim(2)-x(end))*tan(theta) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        xs=[x(end) x(end)+y(end)*cot(mu1) x(end)+y(end)*cot(mu2)];ys=[y(end) 0 0];
        if mu2<0
            xs=[x(end) ui.xlim(2) ui.xlim(2)];ys=[y(end) y(end)-(ui.xlim(2)-x(end))*tan(mu1) y(end)-(ui.xlim(2)-x(end))*tan(mu2)];    
        end
        hwave=fill(xs,ys,[0.85-0.85*tanh(m2-m1) 0.85 1-tanh(m2-m1)]);set(hwave,'Linestyle','none');
       hold off;   
    elseif pbpc==pbpcS
        set(ui.state,'String','Shock at Exit');
        axes(ui.axes(1));hold on; %plot flow and shock
        hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        xs=x(end);m1=meD;
        hshock=plot([xs xs],[0 y(end)],'r');set(hshock,'linewidth',m1,'color',[0.85 0.85-0.85*tanh(m1-1) 1-tanh(m1-1)]);
        hold off
    end    
else %shock in nozzle
    mexit=me(pbpc,aeat,g);
    pep02=pp0(mexit,g);
    p02pc=pbpc/pep02;
    m1=m_p02p01(p02pc,g);
    a1=aas(m1,g);
    up=find(x<0);md=find(x>=0 & y<a1);dn=find(x>0 & y>a1);
    m=[m_aas(y(up),g,0) m_aas(y(md),g,1) m_aas(y(dn)*p02pc,g,0)];
    ppc=pp0(m,g);ppc(dn)=ppc(dn)*p02pc;
    axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
    hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;
    axes(ui.axes(1));hold on; %plot flow and shock
    hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
    xs=x(md(end))+(a1-y(md(end)))/(y(dn(1))-y(md(end)))*(x(dn(1))-x(md(end)));
    hshock=plot([xs xs],[0 a1],'r');set(hshock,'linewidth',m1,'color',[1 1-tanh(m1-1) 1-tanh(m1-1)]);
    hold off
    set(ui.state,'String','Shock in Nozzle');
end
end






% Helper functions below




function pbpcApply (object, eventdata)
global ui flow;
flow.pbpc=get(ui.pbpc,'Value');
flowplot();
set(ui.pbpcV,'String',num2str(flow.pbpc));
set(ui.pbpc,'Value',flow.pbpc);
end

function aeatApply (object, eventdata)
global ui flow;
flow.aeat=get(ui.aeat,'Value');
flowplot();
set(ui.aeatV,'String',num2str(flow.aeat));
set(ui.aeat,'Value',flow.aeat);
end

function gammaApply (object, eventdata)
global ui flow;
flow.g=get(ui.gamma,'Value');
flowplot();
set(ui.gammaV,'String',num2str(flow.g));
set(ui.gamma,'Value',flow.g);
end


% Design regime

function design (object, eventdata)
global ui flow;
flow.pbpc=flow.pbpcD;
flowplot();
set(ui.pbpcV,'String',num2str(flow.pbpc));
set(ui.pbpc,'Value',flow.pbpc);
end

% Subsonic choked

function choked (object, eventdata)
global ui flow;
flow.pbpc=flow.pbpcC;
flowplot();
set(ui.pbpcV,'String',num2str(flow.pbpc));
set(ui.pbpc,'Value',flow.pbpc);
end   

% Supersonic shock

function shockExit (object, eventdata)
global ui flow;
flow.pbpc=flow.pbpcS;
flowplot();
set(ui.pbpcV,'String',num2str(flow.pbpc));
set(ui.pbpc,'Value',flow.pbpc);
end 


% Flow functions


function r=aas(m,g)
r=1./m.*(2/(g+1)*(1+(g-1)/2*m.^2)).^((g+1)/2/(g-1));
end

function r=pp0(m,g)
r=(1+(g-1)/2*m.^2).^(-g/(g-1));
end

function r=p02p01(m,g)
r=((g+1)*m.^2./((g-1)*m.^2+2))^(g/(g-1)).*((g+1)./(2*g*m.^2-(g-1))).^(1/(g-1));
end

function r=p2p1(m,g)
r=1+2*g/(g+1)*(m.^2-1);
end

function n=nu(m,g)
   n=sqrt((g+1)/(g-1))*atan(sqrt((g-1)/(g+1)*(m.^2-1)))-atan(sqrt(m.^2-1));
end

function r=m_pp0(pp0,g)
r=sqrt((pp0.^(-(g-1)/g)-1)*2/(g-1));
end

function m=m_aas(a,g,super)  %super=1 returns supersonic solutions, else subsonic
m=zeros(size(a));
m(find(a<1))=nan;
m(find(a==1))=1;

if super==1
    minit=1e5;
else
    minit=1e-5;
end

for n=1:length(a(:))
    if m(n)==0
        m0=1;m1=minit;
        while(abs(m1-m0)>1e-6)
            m0=m1;
            f=aas(m0,g)-a(n);
            fp=(2/(g+1)*(1+(g-1)/2*m0^2)).^((g+1)/2/(g-1)-1)-aas(m0,g)/m0;
            m1=m0-f/fp;
            if m1<0
                m1=m0/2;
            end
        end
        m(n)=m1;
    end
end
end

function m=m_p02p01(r,g)
m=zeros(size(r));
m(find(r<0 | r>1))=nan;
m(find(r==1))=1;

minit=2;eps=1e-4;
for n=1:length(r(:))
    if m(n)==0
        m0=1;m1=minit;
        while(abs(m1-m0)>eps)
            m0=m1;
            f=p02p01(m0,g)-r(n);f1=p02p01(m0+eps,g)-r(n);
            fp=(f1-f)/eps;
            m1=m0-f/fp;
        end
        m(n)=m1;
    end
end
end

function me=me(pbpc,aeat,g)
%Just choked
meChoke=m_aas(aeat,g,0);
pbpcChoke=pp0(meChoke,g);
%Design
meDesign=m_aas(aeat,g,1);
pbpcDesign=pp0(meDesign,g);
%Shock at exit
pbpcSAE=p2p1(meDesign,g)*pbpcDesign;

if pbpc>=1
    me=0;
elseif pbpc>=pbpcChoke
    me=m_pp0(pbpc,g);
elseif pbpc>pbpcSAE
    me=sqrt(-1/(g-1)+sqrt(1/(g-1)^2+2/(g-1)*(2/(g+1))^((g+1)/(g-1))/aeat^2/pbpc^2));
else
    me=meDesign;
end
end
