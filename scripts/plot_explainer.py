"""Render matched English 3D views of endpoint and all-depth contrasts.

Both figures use the same law family, camera, axes, color normalization and Q.
The all-depth sum equals joint mutual information by the averaged chain rule.
"""
from pathlib import Path
import math
import os
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'generated/.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch
import matplotlib.tri as mtri
import numpy as np
import information_geometry as geo
import premise_metrics as pm

ASSETS = ROOT/'assets'
INK, GRAY, PURPLE = '#172f43', '#526675', '#7558a5'
BG = '#fffefb'
R, S = .70, .25
D = pm.audit(geo.law_at(R,S), (0,1,2), 3)
LAYERS = [v['mean_cmi_bits'] for v in D['conditioning_ladder']]
ELEVATION, AZIMUTH = 16, -25
LIMIT = 2.4
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
    'text.color':INK, 'axes.labelcolor':GRAY, 'xtick.color':GRAY,
    'ytick.color':GRAY, 'figure.facecolor':BG, 'axes.facecolor':BG,
    'savefig.facecolor':BG, 'axes.spines.top':False,
    'axes.spines.right':False, 'pdf.fonttype':42})


def render(rows, endpoint):
    field='omega_D_bits' if endpoint else 'delta_ladder_bits'
    value=D['omega_D_bits'] if endpoint else sum(LAYERS)-D['M_bits']
    symbol=r'\Omega_D' if endpoint else r'\Delta_{\rm all}'
    title='01   Endpoint balance' if endpoint else '02   Including the intermediate level'
    formula=(r'$\Omega_D = F-M = 3(L_0-L_2)$' if endpoint else
             r'$\Delta_{\rm all} = L_0+L_1+L_2-M = I(\mathbf{X};Y)-M$')
    description=('Marginal versus fully conditioned information.' if endpoint else
                 'Equal weight per conditioning depth; an exploratory contrast.')
    fig=plt.figure(figsize=(11.5,8.3))
    fig.text(.055,.948,title,fontsize=25,weight='bold')
    fig.text(.055,.896,formula,fontsize=21)
    fig.text(.055,.861,description,fontsize=12,color=GRAY)
    ax=fig.add_axes([.005,.165,.715,.67],projection='3d',computed_zorder=False)
    r=np.array([v['copy_weight'] for v in rows]);s=np.array([v['parity_weight'] for v in rows]);z=np.array([v[field] for v in rows])
    tri=mtri.Triangulation(r,s)
    norm=TwoSlopeNorm(vmin=-LIMIT,vcenter=0,vmax=LIMIT)
    surf=ax.plot_trisurf(tri,z,cmap='RdBu_r',norm=norm,linewidth=0,
                        antialiased=True,shade=False,zorder=1)
    ax.tricontour(tri,z,levels=[0],colors=[INK],linewidths=2.0,zorder=2)
    ax.plot([0,1,0,0],[0,0,1,0],[-LIMIT]*4,color='#b8c9d3',lw=1.1,zorder=.5)
    ax.scatter([R],[S],[value],s=100,c=INK,edgecolors='white',linewidths=1.8,depthshade=False,zorder=20)
    ax.text(R,S,value+.40,'Q',fontsize=20,weight='bold',zorder=21)
    ax.set(xlim=(0,1),ylim=(0,1),zlim=(-LIMIT,LIMIT),xlabel='Copy weight r',ylabel='Parity weight s',zlabel='Contrast (bits)')
    ax.set_xticks([0,.5,1],['','0.5','1.0']);ax.set_yticks([0,.5,1],['','0.5','1.0']);ax.set_zticks([-2,0,2])
    ax.tick_params(labelsize=11,pad=1)
    ax.xaxis.labelpad=8;ax.yaxis.labelpad=8;ax.zaxis.labelpad=4
    ax.view_init(elev=ELEVATION,azim=AZIMUTH)
    ax.set_proj_type('ortho');ax.set_box_aspect((1,1,.72))
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.fill=False
        axis._axinfo['grid']['color']='#dbe2e5'
        axis._axinfo['grid']['linewidth']=.7
    fig.text(.745,.790,'SAME DISTRIBUTION Q',fontsize=11,weight='bold',color=GRAY)
    fig.text(.745,.750,'70% Copy\n25% Parity\n  5% Additive',fontsize=15,linespacing=1.45,va='top')
    fig.text(.745,.610,'Mean CMI at each depth',fontsize=11,weight='bold')
    for index,(label,c) in enumerate((('none',INK),('one',PURPLE),('both',INK))):
        fig.text(.745,.570-index*.039,f'L{index} ({label}) = {LAYERS[index]:.2f}',fontsize=13,color=c,
                 weight='bold' if index==1 else 'normal')
    card=FancyBboxPatch((.733,.305),.235,.135,transform=fig.transFigure,
                       boxstyle='round,pad=0.013,rounding_size=0.014',
                       edgecolor='#dbe2e5',facecolor='#f4f6f7',linewidth=1)
    fig.add_artist(card)
    fig.text(.752,.408,'$'+symbol+'(Q)$',fontsize=17)
    fig.text(.752,.349,f'{value:+.2f} bit',fontsize=27,weight='bold',
             color='#b24035' if value>0 else '#286d9e')
    interpretation=('The marginal sum\nis larger than M.' if endpoint else
                    'The all-depth sum\nis smaller than M.')
    fig.text(.745,.270,interpretation,fontsize=13,linespacing=1.5,va='top')
    fig.text(.745,.173,'Dark curve: zero contrast',fontsize=10.5,color=GRAY)
    cax=fig.add_axes([.115,.108,.49,.018])
    cb=fig.colorbar(surf,cax=cax,orientation='horizontal',ticks=[-2,-1,0,1,2])
    cb.outline.set_visible(False);cb.ax.tick_params(labelsize=10,length=3)
    fig.text(.115,.141,'NEGATIVE',fontsize=9,color='#286d9e',weight='bold')
    fig.text(.605,.141,'POSITIVE',fontsize=9,color='#b24035',weight='bold',ha='right')
    stem='omega-explained-en' if endpoint else 'omega-surface-guide-en'
    for suffix in ('png','pdf'):
        fig.savefig(ASSETS/f'{stem}.{suffix}',dpi=180,bbox_inches='tight',pad_inches=.18)
    plt.close(fig)



def regional_views():
    # Each region is a full triangular patch with dominant anchor weight >= 0.60.
    # No rescaling of the probabilities or contrasts is introduced.
    specs=[('Copy-dominated',0),('Additive-dominated',2),('Parity-dominated',1)]
    fig=plt.figure(figsize=(17,10))
    fig.text(.035,.965,'How the mixture changes the contrast',fontsize=25,weight='bold')
    fig.text(.035,.925,'Three probability regions • dominant anchor weight ≥ 60% • identical color and height scales',fontsize=13,color=GRAY)
    records=[]
    for col,(title,anchor) in enumerate(specs):
        points=[]
        for i in range(31):
            for j in range(31-i):
                w=[.4*i/30,.4*j/30,.4*(30-i-j)/30]
                w[anchor]+=.6
                audit=pm.audit(geo.law_at(w[0],w[1]),(0,1,2),3)
                points.append((w,audit))
        q=max(points,key=lambda item:abs(item[1]['omega_D_bits']-(item[1]['total_target_information_bits']-item[1]['M_bits'])))
        w,d=q
        records.append({'region':title,'dominant_weight_minimum':.6,'selection':'maximum absolute contrast difference on the declared regional grid',
                        'weights':w,'omega_D_bits':d['omega_D_bits'],
                        'delta_all_bits':d['total_target_information_bits']-d['M_bits']})
        fig.text(.035+col*.325,.877,title,fontsize=17,weight='bold')
        fig.text(.035+col*.325,.846,f'Q: Copy {w[0]:.0%} / Parity {w[1]:.0%} / Additive {w[2]:.0%}',fontsize=10.5,color=GRAY)
        r=np.array([v[0][0] for v in points]);s=np.array([v[0][1] for v in points])
        tri=mtri.Triangulation(r,s)
        for row in range(2):
            ax=fig.add_axes([.008+col*.325,.465-row*.39,.32,.355],projection='3d',computed_zorder=False)
            z=np.array([v[1]['omega_D_bits'] if row==0 else v[1]['total_target_information_bits']-v[1]['M_bits'] for v in points])
            val=d['omega_D_bits'] if row==0 else d['total_target_information_bits']-d['M_bits']
            surf=ax.plot_trisurf(tri,z,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-LIMIT,vcenter=0,vmax=LIMIT),shade=False,linewidth=0,zorder=1)
            if min(z)<0<max(z):
                ax.tricontour(tri,z,levels=[0],colors=[INK],linewidths=1.7,zorder=2)
            ax.scatter([w[0]],[w[1]],[val],c=INK,s=65,edgecolors='white',depthshade=False,zorder=20)
            ax.text(w[0],w[1],val+.40,'Q',fontsize=14,weight='bold',zorder=21)
            label='ΩD' if row==0 else 'Δall'
            ax.set_title(f'{label}(Q) = {val:+.2f} bits',fontsize=15,pad=2,color=INK)
            ax.set(xlim=(min(r)-.015,max(r)+.015),ylim=(min(s)-.015,max(s)+.015),zlim=(-LIMIT,LIMIT))
            ax.set_xlabel('Copy weight',fontsize=10,labelpad=1);ax.set_ylabel('Parity weight',fontsize=10,labelpad=1)
            ax.set_xticks([min(r),max(r)]);ax.set_yticks([min(s),max(s)]);ax.set_zticks([-2,0,2])
            ax.tick_params(labelsize=9,pad=0)
            if col==0: ax.set_zlabel('bits',fontsize=10,labelpad=1)
            # One common camera for every patch and metric.
            ax.view_init(elev=16,azim=-25);ax.set_proj_type('ortho');ax.set_box_aspect((1,1,.8))
            for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
                axis.pane.fill=False;axis._axinfo['grid']['color']='#dbe2e5'
    cax=fig.add_axes([.28,.033,.44,.015])
    cb=fig.colorbar(surf,cax=cax,orientation='horizontal',ticks=[-2,-1,0,1,2]);cb.outline.set_visible(False)
    for suffix in ('png','pdf'):
        fig.savefig(ASSETS/f'omega-mixture-regions-en.{suffix}',dpi=180,bbox_inches='tight',pad_inches=.18)
    plt.close(fig)
    import json
    (ROOT/'results/geometry/regional-extremes.json').write_text(json.dumps({'regional_resolution':30,'regions':records},indent=2)+'\n')


def main():
    rows=geo.grid()
    for row in rows:
        assert math.isclose(row['delta_ladder_bits']+row['M_bits'],row['total_information_bits'],abs_tol=1e-11)
    assert math.isclose(sum(LAYERS),D['total_target_information_bits'],abs_tol=1e-11)
    render(rows,True);render(rows,False);regional_views()
    print('Rendered two matched English 3D figures. Verified the chain-rule identity at all 1,081 grid points.')
    print({'Q':(R,S,1-R-S),'means':LAYERS,'omega_D':D['omega_D_bits'],
           'delta_all':sum(LAYERS)-D['M_bits']})


if __name__=='__main__':
    main()
