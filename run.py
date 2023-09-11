import glob
import streamlit as st
import pyaudacity as pa
import sys



if 'counter' not in st.session_state: 
    st.session_state.counter = 0
    st.session_state.label = 0

def reset(val, x):
    i, _ = val
    st.session_state.counter = i
    st.session_state.label = x

def record():
    pa.record1st_choice()

def reset_to_last():
    pa.stop()
    pa.do('MoveToPrevLabel')
    pa.do('PunchAndRoll')
    
def showPhoto(photo, skip):
    st.write(f"Index as a session_state attribute: {st.session_state.counter}")
    st.write(f"Label: {st.session_state.label}")

    if not skip:
        print(pa.do('AddLabelPlaying'))
        pa.do(f'SetLabel: Label="{st.session_state.label}" Text="{photo}"')
        pa.do(f'Select:End="0 Mode="Set" RelativeTo="ProjectStart" Start="0"')
        pa.record1st_choice()
        st.session_state.label += 1    
    ## Increments the counter to get next photo
    st.session_state.counter += 1

        
ls = list([j for i,j in enumerate(sorted(list(glob.glob(f"slides/{sys.argv[1]}*.png"))))])
           # if int(j.split("-")[1].split(".")[0]) % 2 == 0])

# Get list of images in folder

st.subheader("List of images in folder")
out = st.selectbox(label="slides", options=enumerate(ls))
x = st.number_input(label="label", value=st.session_state.label)
st.button("Reset", on_click=reset, args=[out, x])

# st.write(ls)

# Select photo a send it to button

photo = ls[st.session_state.counter]
st.image(photo,caption=photo)

c1, c2, c3, c4 = st.columns(4)
show_btn = c1.button("Next", on_click=showPhoto,args=([photo, False]))
show_btn = c2.button("Skip", on_click=showPhoto,args=([photo, True]))
show_btn = c3.button("Record", on_click=record)
show_btn = c4.button("Again", on_click=reset_to_last)

photo_next = ls[st.session_state.counter + 1]
st.image(photo_next, caption=photo_next, width=200)

