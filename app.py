import streamlit as st
import pandas as pd
st.set_page_config(page_title='현대오토에버 사업별 내부회계 분석',page_icon='🛡️',layout='wide')
st.title('🛡️ 현대오토에버 사업별 내부회계 통제 시뮬레이터')
st.caption('SI · ITO · 차량 SW | 공시 기반 사업 분석 + 가상 통제 운영평가')
st.warning('교육·자기소개서 연구용입니다. 실제 현대오토에버 내부회계 미비점이나 회계오류를 평가하지 않습니다. 통제 데이터는 전부 가상입니다.')
segments={'SI':{'description':'기업 정보시스템의 설계·구축, ERP·스마트팩토리·클라우드 프로젝트','risk':'계약 변경, 검수 및 매출 인식 근거, 추정원가 변경의 승인','controls':['계약 변경 승인','매출 인식 근거 검토','원가 추정 변경 승인','매출액 산정 재계산'],'evidence':'계약서, 변경승인, 검수 문서, 원가 산정표'},'ITO':{'description':'고객 전산시스템 운영·관리·유지보수','risk':'서비스 제공 기간, 청구 누락, 계약 단가 불일치','controls':['서비스 수행기록 대사','청구 금액·단가 검증','계약 변경 승인','청구 누락 검토'],'evidence':'운영기록, 계약서, 청구 명세서'},'차량 SW':{'description':'AUTOSAR 기반 mobilgene 플랫폼, 내비게이션 SW 공급','risk':'계약상 납품·검수 조건 및 개발지출 회계처리','controls':['납품·검수 근거 확인','계약별 수익 인식 조건 검토','개발지출 분류 검토','회계처리 승인'],'evidence':'SW 계약서, 납품·검수 문서, 개발비 지출내역'}}
sales=pd.DataFrame([['2024 연간',16303.88751,12788.69352,8043.59174],['2025 연간',17671.73268,16571.92189,8277.01804],['2025 상반기',7650.48161,6874.42598,4225.71499],['2026 상반기',9088.07340,8674.01625,4102.38098]],columns=['기간','ITO','SI','차량 SW'])
rows=[]
for biz,d in segments.items():
 for i,c in enumerate(d['controls']):
  rows.append([f'{biz}-{i+1:02d}',biz,c,True,i%3!=1,'완료','미완료' if i==2 else '완료'])
if 'review' not in st.session_state:st.session_state.review=pd.DataFrame(rows,columns=['점검ID','사업','통제활동','수행여부','증빙확보','기대결과','실제기록'])
def evaluate(df):
 d=df.copy();d['수행누락']=~d['수행여부'].fillna(False).astype(bool);d['증빙누락']=~d['증빙확보'].fillna(False).astype(bool);d['기록불일치']=d['기대결과'].astype(str)!=d['실제기록'].astype(str)
 d['점검사유']=d.apply(lambda r:', '.join(k for k in ['수행누락','증빙누락','기록불일치'] if r[k]) or '입력자료상 특이사항 없음',axis=1)
 d['추가확인']=d[['수행누락','증빙누락','기록불일치']].any(axis=1)
 return d
t1,t2,t3,t4,t5=st.tabs(['① 사업구조 분석','② 사업별 리스크·통제','③ 운영평가 시뮬레이션','④ 개선 시나리오','⑤ 평가 요약·지원동기'])
with t1:
 st.header('왜 현대오토에버인가?')
 st.write('현대오토에버는 **시스템 구축(SI), 운영·유지보수(ITO), 차량 SW**를 함께 영위합니다. 서로 다른 사업의 계약·회계 프로세스를 이해하고 사업별로 적합한 통제를 설계하는 문제의식에서 출발했습니다.')
 period=st.selectbox('공시 매출 비교 기간',sales['기간'],index=3)
 a=sales[sales['기간']==period].iloc[0];chart=pd.DataFrame({'사업':['ITO','SI','차량 SW'],'매출액(억원)':[a['ITO'],a['SI'],a['차량 SW']]})
 st.bar_chart(chart.set_index('사업'));st.dataframe(chart.round(1),hide_index=True,use_container_width=True)
 prev=sales[sales['기간']=='2025 상반기'].iloc[0];cur=sales[sales['기간']=='2026 상반기'].iloc[0]
 for col,biz in zip(st.columns(3),['SI','ITO','차량 SW']):col.metric(f'{biz} 전년동기 매출증감',f'{(cur[biz]/prev[biz]-1)*100:+.1f}%')
 st.caption('출처: 현대오토에버 2026.08.14 반기보고서 Ⅱ. 사업의 내용, 주요 제품 및 서비스. 매출액은 연결기준 공시 천원 단위를 억원으로 환산. 매출 증가가 통제 위험 증가를 의미하지는 않습니다.')
with t2:
 biz=st.selectbox('사업 선택',list(segments));d=segments[biz]
 st.subheader('사업별 위험-통제 매핑(RCM 기초)')
 st.write('**사업 특성:**',d['description']);st.write('**잠재 점검 영역:**',d['risk'])
 for i,c in enumerate(d['controls'],1):st.write(f'{i}. {c}')
 st.write('**증빙 예시:**',d['evidence'])
 st.info('잠재 위험과 통제활동은 일반적인 회계·내부통제 원리에 따른 교육용 가정이며 실제 현대오토에버 RCM을 확인한 결과가 아닙니다.')
with t3:
 st.subheader('사업별 가상 통제 점검표')
 st.write('가상 통제 12개를 직접 편집하고 통제 수행, 증빙, 기대 결과와 실제 기록의 차이를 확인합니다.')
 edited=st.data_editor(st.session_state.review,num_rows='dynamic',hide_index=True,use_container_width=True,key='edit');st.session_state.review=edited.copy()
 result=evaluate(edited);c1,c2=st.columns(2);c1.metric('점검 항목 수',len(result));c2.metric('추가 확인 항목 수',int(result['추가확인'].sum()))
 st.dataframe(result[['점검ID','사업','통제활동','점검사유']],hide_index=True,use_container_width=True)
 st.caption('점검 사유는 추가 확인을 위한 신호이지 실제 통제 미비점 확정 판정이 아닙니다.')
with t4:
 st.subheader('가정한 개선조치 전후 비교')
 actions=st.multiselect('적용할 개선 가정',['통제 수행 완료','증빙 확보','기록 불일치 수정'],default=['증빙 확보'])
 before=evaluate(st.session_state.review);after_data=st.session_state.review.copy()
 if '통제 수행 완료' in actions:after_data['수행여부']=True
 if '증빙 확보' in actions:after_data['증빙확보']=True
 if '기록 불일치 수정' in actions:after_data['실제기록']=after_data['기대결과']
 after=evaluate(after_data);comparison=pd.DataFrame({'시나리오':['개선 전','개선 후(가정)'],'추가 확인 수':[int(before['추가확인'].sum()),int(after['추가확인'].sum())]})
 st.bar_chart(comparison.set_index('시나리오'));st.dataframe(comparison,hide_index=True)
 st.warning('개선 후 결과는 가상 데이터를 변경한 산술적 비교이며 실제 운영효과성 개선의 증거가 아닙니다.')
with t5:
 st.subheader('사업별 점검 결과 요약')
 result=evaluate(st.session_state.review);summary=result.groupby('사업',as_index=False).agg(점검수=('점검ID','count'),추가확인수=('추가확인','sum'),수행누락=('수행누락','sum'),증빙누락=('증빙누락','sum'),기록불일치=('기록불일치','sum'))
 st.dataframe(summary,hide_index=True,use_container_width=True)
 st.download_button('상세 점검 결과 CSV',result.to_csv(index=False).encode('utf-8-sig'),file_name='business_control_details.csv')
 st.download_button('사업별 요약 CSV',summary.to_csv(index=False).encode('utf-8-sig'),file_name='business_control_summary.csv')
 st.subheader('점검 이후 실무에서 필요한 절차')
 st.write('증빙·승인 이력 확인 → 현업부서와 예외 원인 확인 → 통제 설계 및 운영 평가 → 개선조치 → 재점검·문서화')
 st.subheader('지원동기 연결')
 st.write('**왜 현대오토에버:** SI·ITO·차량 SW라는 서로 다른 사업을 함께 영위하므로 사업별 프로세스를 이해하는 내부통제 업무의 폭이 넓다고 판단했습니다.')
 st.write('**왜 내부회계:** 숫자에 나타난 결과의 분석을 넘어 회계정보가 생성되는 과정에서 위험을 예방·발견하는 통제활동에 관심을 가졌습니다.')
 st.write('**커리어 계획:** 통제활동 문서화와 운영평가를 익힌 뒤, 데이터 분석과 현업 협력을 통해 사업별 통제를 개선하고 연결 내부회계관리제도까지 전문성을 넓히겠습니다.')
