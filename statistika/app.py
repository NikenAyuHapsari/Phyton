with tab2:
    st.header("Visualisasi Distribusi Data")

    col_hist, col_box = st.columns(2)
    
    with col_hist:
        st.subheader("Histogram (Distribusi Frekuensi)")
        
        # Plotly Histogram (Kode Plotly tetap sama)
        df_plot = pd.DataFrame({'Nilai': data_np})
        fig_hist = px.histogram(
            df_plot, 
            x="Nilai", 
            nbins=bins, 
            title="Histogram Data",
            labels={'Nilai':'Nilai Data'},
            color_discrete_sequence=['teal']
        )
        fig_hist.update_layout(bargap=0.05, height=450)
        st.plotly_chart(fig_hist, use_container_width=True)
        # Hapus atau jadikan komentar tag berikut:
        # with col_box:
        st.subheader("Box Plot (Diagram Kotak Garis)")
        
        # Plotly Box Plot (Kode Plotly tetap sama)
        fig_box = px.box(
            df_plot, 
            y="Nilai", 
            title="Box Plot Data",
            color_discrete_sequence=['maroon']
        )
        fig_box.update_layout(height=450)
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown("Box Plot menunjukkan **Median** (garis tengah), **Kuartil 1 & 3** (tepi kotak), dan **Nilai Minimum/Maksimum** (garis sumbu).")
        # Hapus atau jadikan komentar tag berikut:
        # 

[Image of a box plot illustrating quartiles and median]
