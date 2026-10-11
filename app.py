import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title='Global ERP Internal Control Analyzer',page_icon='🛡️',layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem}.small-note{color:#667085;font-size:.88rem}.stMetric{background:#f6f8fb;padding:12px;border-radius:10px}</style>''',unsafe_allow_html=True)
st.title('🛡️ Global ERP Internal Control Analyzer')
st.caption('현대오토에버 지원 직무 연구용 | 글로벌 ERP 환경의 내부회계 통제 점검 시뮬레이터')
st.warning('본 프로그램은 지원자가 학습 목적으로 개발한 가상 시뮬레이터입니다. 현대오토에버 또는 고객사의 실제 ERP 데이터, 통제 설계·운영 상태, 감사 결과를 평가하지 않습니다.')

SAMPLE=[
 ('TX001','한국','매입','V101','2026-06-01',12000000,12000000,'승인','있음','U01','U02'),
 ('TX002','미주','매입','V102','2026-06-02',8800000,8800000,'미승인','있음','U03','U04'),
 ('TX003','유럽','매입','V103','2026-06-03',5500000,5500000,'승인','없음','U05','U06'),
 ('TX004','아태','매입','V104','2026-06-04',7200000,6900000,'승인','있음','U07','U08'),
 ('TX005','한국','매입','V105','2026-06-05',15000000,15000000,'승인','있음','U09','U09'),
 ('TX006','미주','매입','V106','2026-06-06',4400000,4400000,'승인','있음','U10','U11'),
 ('TX007','미주','매입','V106','2026-06-06',4400000,4400000,'승인','있음','U10','U11'),
 ('TX008','유럽','매입','V107','2026-06-07',9800000,9800000,'승인','있음','U12','U13'),
 ('TX009','아태','매입','V108','2026-06-08',6000000,6000000,'미승인','없음','U14','U14'),
 ('TX010','한국','매입','V109','2026-06-09',3100000,3100000,'승인','있음','U15','U16'),
]
COLS=['거래ID','지역','거래유형','거래처코드','거래일','ERP기록금액','증빙금액','승인상태','증빙유무','입력자','승인자']

def assess(df, checks):
    d=df.copy()
    d['승인누락']= (d['승인상태']!='승인') if checks['approval'] else False
    d['증빙누락']= (d['증빙유무']!='있음') if checks['evidence'] else False
    d['금액불일치']= (d['ERP기록금액']!=d['증빙금액']) if checks['amount'] else False
    d['직무분리위반']= (d['입력자']==d['승인자']) if checks['sod'] else False
    keys=['지역','거래유형','거래처코드','거래일','ERP기록금액']
    d['중복의심']=d.duplicated(subset=keys,keep=False) if checks['duplicate'] else False
    flags=['승인누락','증빙누락','금액불일치','직무분리위반','중복의심']
    d['탐지항목수']=d[flags].sum(axis=1)
    d['점검결과']=d['탐지항목수'].map(lambda x:'추가 점검 필요' if x else '설정 규칙상 특이사항 없음')
    d['점검사유']=d.apply(lambda r:', '.join(k for k in flags if r[k]) or '없음',axis=1)
    return d,flags

DEFAULT={'approval':True,'evidence':True,'amount':True,'sod':True,'duplicate':True}
if 'data' not in st.session_state: st.session_state.data=pd.DataFrame(SAMPLE,columns=COLS)
if 'checks' not in st.session_state: st.session_state.checks=DEFAULT.copy()

t1,t2,t3,t4,t5=st.tabs(['① 개발 배경·사용법','② 거래 프로세스·데이터','③ 내부통제 점검','④ 통제 개선 시뮬레이션','⑤ 평가 요약·다운로드'])
with t1:
    st.header('왜 이 프로그램을 만들었나요?')
    st.write('현대오토에버는 현대차그룹의 글로벌 차세대 ERP 구축·확산 사업을 수행합니다. ERP는 구매·승인·증빙·회계기록 등 업무 프로세스를 연결하므로, 거래가 회계정보로 기록되는 과정에서 발생 가능한 위험을 이해하는 데 좋은 연구 사례입니다.')
    st.info('**핵심 구분:** 현대오토에버가 고객사를 위해 수행하는 ERP 구축 사업과 현대오토에버 자체의 연결 내부회계관리제도는 서로 다른 대상입니다. 이 프로그램은 고객사나 현대오토에버의 실제 통제 효과성을 판단하지 않습니다.')
    st.subheader('어떻게 분석하나요?')
    st.markdown('**①** 가상 거래 10건을 확인합니다.  **②** 승인·증빙·금액·직무분리·중복 여부를 규칙으로 점검합니다.  **③** 통제 규칙을 변경해 탐지 결과의 차이를 비교합니다.  **④** 점검 결과를 CSV로 내려받습니다.')
    st.subheader('무엇을 배울 수 있나요?')
    st.write('동일한 거래라도 어떤 통제활동을 적용하는지에 따라 탐지되는 위험 징후가 달라집니다. 따라서 내부회계관리에서는 수치의 결과뿐 아니라 거래의 승인, 증빙, 기록 및 사후 검토 과정이 중요합니다. 탐지된 징후는 오류나 통제 미비점의 확정 판정이 아니며 원인 확인과 추가 증빙 검토가 필요합니다.')
    st.subheader('공시와 시뮬레이션의 구분')
    st.markdown('- **공시에서 확인할 사항:** 현대차 차세대 ERP 본사·미주 및 아태·유럽 확산 프로젝트, 해외 연결대상 종속기업, 내부회계관리제도 감사 의견\n- **가상 가정:** 아래 거래 10건, 통제 규칙, 점검 결과 및 개선 시나리오\n- **분석 한계:** 실제 RCM, ERP 로그, 접근권한 정책, 계약서, 회계전표, 감사증거를 확보하지 않았으므로 실효성 평가 불가')
    st.caption('참고자료: 현대오토에버 2025년 사업보고서 및 2026년 반기보고서. 공시 수치는 프로그램 내 거래자료와 혼용하지 않습니다.')
with t2:
    st.header('거래에서 회계정보까지')
    st.markdown('**거래 발생 → 담당자 입력 → 권한 있는 담당자 승인 → 증빙 확인 → ERP 회계기록 → 사후 대사·모니터링**')
    st.write('아래 데이터는 모두 가상입니다. 편집하면 나머지 탭에 자동 반영됩니다.')
    df=st.data_editor(st.session_state.data,num_rows='dynamic',use_container_width=True,hide_index=True,key='editor')
    st.session_state.data=df.copy()
    st.download_button('가상 거래 원본 CSV 다운로드',data=df.to_csv(index=False).encode('utf-8-sig'),file_name='sample_erp_transactions.csv',mime='text/csv')
    st.caption('거래ID는 고유 식별자입니다. 중복의심은 거래ID가 아니라 지역·유형·거래처·일자·금액의 조합으로 판단합니다.')
with t3:
    st.header('통제활동별 점검')
    st.write('점검 항목을 선택하고 아래 결과를 확인하세요. 비활성화된 항목은 탐지하지 않습니다.')
    a,b,c=st.columns(3)
    with a:
        st.session_state.checks['approval']=st.checkbox('승인 누락 탐지',value=st.session_state.checks['approval'])
        st.session_state.checks['evidence']=st.checkbox('증빙 누락 탐지',value=st.session_state.checks['evidence'])
    with b:
        st.session_state.checks['amount']=st.checkbox('ERP·증빙 금액 불일치 탐지',value=st.session_state.checks['amount'])
        st.session_state.checks['sod']=st.checkbox('입력자·승인자 동일 탐지',value=st.session_state.checks['sod'])
    with c: st.session_state.checks['duplicate']=st.checkbox('중복 거래 의심 탐지',value=st.session_state.checks['duplicate'])
    result,flags=assess(st.session_state.data,st.session_state.checks)
    n=int((result['탐지항목수']>0).sum())
    x,y,z=st.columns(3)
    x.metric('전체 거래',len(result));y.metric('추가 점검 대상',n);z.metric('탐지 항목 합계',int(result['탐지항목수'].sum()))
    st.dataframe(result[['거래ID','지역','ERP기록금액','점검결과','점검사유']],hide_index=True,use_container_width=True)
    st.bar_chart(result[flags].sum().rename({'승인누락':'승인 누락','증빙누락':'증빙 누락','금액불일치':'금액 불일치','직무분리위반':'직무분리','중복의심':'중복 의심'}))
    st.caption('동일 거래에 여러 징후가 중복 탐지될 수 있습니다. 탐지 건수는 확정 오류 건수가 아닙니다.')
with t4:
    st.header('통제 규칙 적용 전후 비교')
    st.write('비교 기준은 ① 승인·증빙만 점검하는 기본 시나리오, ② 다섯 가지 점검을 모두 적용하는 확대 시나리오입니다.')
    base,_=assess(st.session_state.data,{'approval':True,'evidence':True,'amount':False,'sod':False,'duplicate':False})
    enhanced,flags=assess(st.session_state.data,DEFAULT)
    v1=int((base['탐지항목수']>0).sum());v2=int((enhanced['탐지항목수']>0).sum())
    c1,c2,c3=st.columns(3)
    c1.metric('기본 규칙 탐지 거래',v1)
    c2.metric('확대 규칙 탐지 거래',v2)
    c3.metric('추가로 발견한 점검 대상',v2-v1)
    comparison=pd.DataFrame({'기본 규칙':base[flags].sum(),'확대 규칙':enhanced[flags].sum()})
    st.bar_chart(comparison)
    st.info('탐지 항목이 증가한 것은 점검 범위가 넓어졌다는 의미이지, 통제 품질이 향상되었거나 실제 오류가 감소했다는 증거는 아닙니다. 개선 효과는 실제 운영 증빙과 사후 재점검으로 검증해야 합니다.')
    st.subheader('권장 통제 설계 예시')
    st.dataframe(pd.DataFrame([
      ['승인 누락','전표 확정 전 승인 상태 확인','승인 로그 및 권한자 목록'],
      ['증빙 누락','증빙 첨부 필수 및 누락 예외 검토','전자증빙·예외 승인 기록'],
      ['금액 불일치','ERP 금액과 원천증빙 자동 대사','대사 내역 및 차이 조정 승인'],
      ['직무분리','입력·승인 권한 분리 및 예외 승인','권한 매트릭스·변경 로그'],
      ['중복 의심','거래처·일자·금액 조합 중복 경고','중복 경고 처리 이력']
    ],columns=['위험 징후','통제활동 예시','평가 증빙 예시']),hide_index=True,use_container_width=True)
with t5:
    st.header('내부회계 점검 결과 요약')
    result,flags=assess(st.session_state.data,st.session_state.checks)
    st.write(f"총 **{len(result)}건** 중 **{int((result['탐지항목수']>0).sum())}건**에서 추가 점검할 징후가 확인되었습니다(현재 선택된 규칙 기준).")
    summary=pd.DataFrame({'점검 항목':flags,'탐지 건수':[int(result[f].sum()) for f in flags]})
    st.dataframe(summary,hide_index=True,use_container_width=True)
    st.markdown('**권장 후속 절차:** 탐지 거래 원천증빙 확인 → 실제 승인·처리 이력 확인 → 예외 사유 확인 → 통제 설계 또는 운영상 개선 필요성 판단 → 개선 후 재점검')
    st.download_button('상세 점검 결과 CSV 다운로드',data=result.to_csv(index=False).encode('utf-8-sig'),file_name='erp_internal_control_assessment.csv',mime='text/csv')
    st.download_button('점검 요약 CSV 다운로드',data=summary.to_csv(index=False).encode('utf-8-sig'),file_name='erp_control_summary.csv',mime='text/csv')
    st.caption('본 결과는 시뮬레이션 결과로서 실제 내부회계 평가보고서나 감사의견을 대체하지 않습니다.')
