import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

import helper

# Load the dataset
import pandas as pd
temp = pd.read_csv('clean_dataset.csv')

#### Global Variables
team_list = ['Overall'] + list(temp['team1'].unique())
year_list = ['Overall'] + list(temp['season'].unique())
match_list= ['Overall'] + list(temp['match_type'].unique())


## Page Information
st.set_page_config(page_title="IPL Analysis", page_icon=":smiley:")

## Home Page Information
select_option = st.sidebar.selectbox("Filter By", ["Overall", "Team","match_type"])


##############################################################################################
## Overall Data Analysis
if select_option=='Overall':
    st.title('Overall IPL Data Analysis')

    ##########
    st.markdown('### Kaggle Dataset')
    st.dataframe(temp)

    ##########
    teams = pd.concat([temp['team1'], temp['team2']]).unique()
    team_stats = pd.DataFrame(teams, columns=['team_name'])
    st.markdown("### List of Teams in IPL History")
    st.table(team_stats)


    ##########
    st.markdown('### Top 10 players with the most "Man of the Match" awards')
    man_of_the_match_counts = temp['player_of_match'].value_counts().reset_index()
    man_of_the_match_counts.columns = ['player', 'awards']
    top_man_of_the_match = man_of_the_match_counts.head(10)
    
    chart = alt.Chart(top_man_of_the_match).mark_bar().encode(
    x='player:N',
    y='awards:Q',
    color=alt.Color('player:N', legend=None)
    ).properties(
    width=600,
    height=400
    ).configure_axisX(
    labelAngle=45
    )
    st.altair_chart(chart)

    ##########
    st.markdown('### Teams Performance Statistics')
    team_stats['matches_played'] = team_stats['team_name'].apply(lambda x: len(temp[(temp['team1'] == x) | (temp['team2'] == x)]))
    team_stats['matches_won'] = team_stats['team_name'].apply(lambda x: len(temp[temp['winner'] == x]))
    team_stats['win_percentage'] = (team_stats['matches_won'] / team_stats['matches_played']) * 100

    st.table(team_stats)



##############################################################################################
if select_option=='Team':
    st.title('IPL Data Analysis by Team')

    Team_name=st.sidebar.selectbox('Select Team', team_list)
    Team_year=st.sidebar.selectbox('Select Year', year_list)

    if Team_name=='Overall' and Team_year=='Overall':
        st.markdown('### Overall Team Analysis')


        st.markdown('##### Total Run score by Team in IPL History')
        df1=temp.groupby('team1')['target_runs'].sum().reset_index().sort_values(by='target_runs',ascending=False)
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(df1['team1'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title('Total Runs by Team', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Total Runs', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=df1, x='team1', y='target_runs', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)



        st.markdown('##### Maximum Run score by Team in IPL History')
        df1=temp.groupby('team1')['target_runs'].max().reset_index().sort_values(by='target_runs',ascending=False)
        sns.set(style="darkgrid")
        palette = sns.color_palette("Set2", n_colors=len(df1['team1'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title('Maximum Target Runs by Team', fontsize=18, fontweight='bold', color='crimson', pad=20)
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='orange', labelpad=10)
        plt.ylabel('Target Runs', fontsize=14, fontweight='bold', color='orange', labelpad=10)
        ax = sns.barplot(data=df1, x='team1', y='target_runs', palette=palette)
        plt.xticks(rotation=90, fontsize=12, fontweight='bold', color='lightblue')
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.grid(True, axis='y', linestyle='--', color='gray', linewidth=0.8)
        plt.tight_layout()
        st.pyplot(plt)


        st.markdown('##### Minimum Run score by Team in IPL History')
        df1=temp.groupby('team1')['target_runs'].min().reset_index().sort_values(by='target_runs',ascending=True)
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(df1['team1'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title('Minimum Target Runs by Team', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Target Runs', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=df1, x='team1', y='target_runs', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)

    if Team_name=='Overall' and Team_year!='Overall':
        st.markdown(f"##### Filter Dataset By {Team_year}")
        Team_year=int(Team_year)
        group_by_year=helper.group_by_year(temp,Team_year)
        st.dataframe(group_by_year)

        semi_final_df=group_by_year.copy()
        max_run_by_year=group_by_year.copy()
        max_MOM_by_year=group_by_year.copy()
        final_df=group_by_year.copy()
        min_run_by_year=group_by_year.copy()




        st.markdown("##### Maximun Run made by Teams")
        max_run_by_year=max_run_by_year.groupby('winner')['target_runs'].max().reset_index()
        max_run_by_year=max_run_by_year.sort_values(by='target_runs',ascending=False)
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(max_run_by_year['winner'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title(f'Maximun Run made by Teams in {Team_year}', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Target Runs', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=max_run_by_year, x='winner', y='target_runs', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)



        st.markdown("##### Minimum Run made by Teams")
        min_run_by_year=min_run_by_year.groupby('winner')['target_runs'].min().reset_index()
        min_run_by_year=min_run_by_year.sort_values(by='target_runs',ascending=True)
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(min_run_by_year['winner'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title(f'Minimum Run made by Teams in {Team_year}', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Target Runs', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=min_run_by_year, x='winner', y='target_runs', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)



        st.markdown("##### Man of the Match Counting")
        max_MOM_by_year=max_MOM_by_year.groupby('player_of_match')['player_of_match'].value_counts().reset_index().sort_values(by='count',ascending=False).iloc[:10]
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(max_MOM_by_year['player_of_match'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title(f'Man of the Match counting in {Team_year}', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Player Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Count', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=max_MOM_by_year, x='player_of_match', y='count', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)



        ### Semi Final details
        st.markdown("##### Semi Final Details")
        semi_final_df=semi_final_df[(semi_final_df['match_type']!='League') & (semi_final_df['match_type']!='Final')]
        semi_final_df=semi_final_df[['season','city','player_of_match','team1','team2','winner','result_margin','target_runs']]

        st.dataframe(semi_final_df)



        ### Final Details

        st.markdown("##### Final Details")
        final_df=final_df[final_df['match_type']=='Final']
        final_df=final_df[['season','city','player_of_match','team1','team2','winner','result_margin','target_runs']]
        final_winners=final_df['winner'].iloc[0]
        final_winner_margin=final_df['result_margin'].iloc[0]
        st.dataframe(final_df)
        st.markdown(f"## {final_winners} won by {final_winner_margin} runs in {Team_year}")











    if Team_name!='Overall' and Team_year=='Overall':
        st.markdown('#### Teams Performance in IPL history')
        team_performance_df=temp.groupby('winner').count().reset_index().sort_values(by='city',ascending=False)[['winner','id']]
        sns.set(style="whitegrid") 
        palette = sns.color_palette("coolwarm", n_colors=len(team_performance_df['winner'].unique()))
        plt.figure(figsize=(12, 10))
        plt.title(f'Matches Won by teams in IPL history', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Team Name', fontsize=14, fontweight='bold', color='darkgreen')
        plt.ylabel('Matches won in Whole IPL', fontsize=14, fontweight='bold', color='darkgreen')
        ax = sns.barplot(data=team_performance_df, x='winner', y='id', palette=palette)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 9), 
                        textcoords='offset points', fontsize=12, fontweight='bold', color='red')
        plt.xticks(rotation=90, fontsize=12, ha='right', color='purple')
        plt.grid(True, axis='y', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)


        st.markdown("### Functionality not completed")
        st.markdown("This feature is currently under development. I'll be implementing it soon.")





    




    if Team_name!='Overall' and Team_year!='Overall':
        st.markdown("### Functionality not yet implemented")
        st.markdown("This feature is currently under development. I'll be implementing it soon.")




































##############################################################################################
if select_option=='match_type':
    st.title('IPL Data Analysis by Match Type')
    match_type=st.sidebar.selectbox('Select Match Type', match_list)
    if match_type=='League':
        league_df=temp[temp['match_type']=='League']
        high_run_df=league_df[league_df['target_runs']==league_df['target_runs'].max()][['season','city','player_of_match','winner','target_runs']]
        min_run_df=league_df[league_df['target_runs']==league_df['target_runs'].min()][['season','city','player_of_match','winner','target_runs']]
        st.markdown(f"#### Highest Runs {high_run_df['target_runs'].iloc[0]} made by {high_run_df['winner'].iloc[0]} in {high_run_df['season'].iloc[0]}")
        st.dataframe(high_run_df)
        st.markdown(f"#### Minimum Runs {min_run_df['target_runs'].iloc[0]} made by {min_run_df['winner'].iloc[0]} in {min_run_df['season'].iloc[0]}")
        st.dataframe(min_run_df)

        st.markdown("### Some Functionality still pending. I'll be implementing it soon.")

    elif match_type=='Final':
        Final_df=temp[temp['match_type']=='Final']
        high_run_df=Final_df[Final_df['target_runs']==Final_df['target_runs'].max()][['season','city','player_of_match','winner','target_runs']]
        min_run_df=Final_df[Final_df['target_runs']==Final_df['target_runs'].min()][['season','city','player_of_match','winner','target_runs']]
        st.markdown(f"#### Highest Runs {high_run_df['target_runs'].iloc[0]} made by {high_run_df['winner'].iloc[0]} in {high_run_df['season'].iloc[0]}")
        st.dataframe(high_run_df)
        st.markdown(f"#### Minimum Runs {min_run_df['target_runs'].iloc[0]} made by {min_run_df['winner'].iloc[0]} in {min_run_df['season'].iloc[0]}")
        st.dataframe(min_run_df)

        st.markdown("### Some Functionality still pending. I'll be implementing it soon.")
    else:
        st.markdown("### Functionality not yet implemented")
        st.markdown("This feature is currently under development. I'll be implementing it soon.")