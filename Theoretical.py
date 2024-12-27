import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Dist_config import *
from Calculator2 import *
from CTkMenuBar import CTkMenuBar



class DistributionVisualizer:
    def __init__(self):
        #initialize user's interface 
        self.root = ctk.CTk()
        self.root.title("Distribution Visualizer")
        self.root.geometry("800x700")
        
        #other params
        self.current_dist = DISTRIBUTIONS['normal']
        self.value_labels = []
        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        #contact us toolbar
        menu = CTkMenuBar(self.root)
        menu.add_cascade("Contact Us", command= self.contact_us)


        # Distribution selector
        selector_frame = ctk.CTkFrame(self.root)
        selector_frame.pack(pady=10, fill='x', padx=10)
        
        ctk.CTkLabel(selector_frame, text="Distribution:").pack(side='left', padx=5)
        self.selector = ctk.CTkComboBox(
            selector_frame,
            values=[dist.name for dist in DISTRIBUTIONS.values()],
            command=self.update_dist,
            width=200
        )
        self.selector.set('Normal (Bell Curve)')
        self.selector.pack(side='left', padx=5)
        
        # Calculator button
        self.calc_button = ctk.CTkButton(
            selector_frame,
            text="Open Calculator",
            command=self.open_calculator
        )
        self.calc_button.pack(side='right', padx=5)

        # Parameter sliders frame
        self.param_frame = ctk.CTkFrame(self.root)
        self.param_frame.pack(pady=10, fill='x', padx=10)
        self.sliders = []
        self.create_sliders()

        # Plot frame
        self.setup_plot()
        self.update_plot()

    def open_calculator(self):
        CalculatorWindow(self.current_dist)

    def contact_us(self):
        self.popup = ctk.CTkToplevel(self.root)
        self.popup.geometry("300x200")
        self.popup.title("Contact Us")       
        self.contact_label = ctk.CTkLabel(self.popup, text="Group 1\nDeveloper: Long Pham\nPhone: +84 .....\nEmail: ...@gmail.com", justify="center")
        self.contact_label.pack(pady=20, padx=20)     

    def create_sliders(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.sliders = []
        self.value_labels = []
        
        ctk.CTkLabel(self.param_frame, text="Parameter").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.param_frame, text="Value").grid(row=0, column=2, padx=5, pady=5)
        
        for i, (param, initial) in enumerate(zip(
            self.current_dist.params,
            self.current_dist.initial_values
        ), start=1):
            ctk.CTkLabel(self.param_frame, text=param).grid(row=i, column=0, padx=5, pady=5)
            
            slider = ctk.CTkSlider(
                self.param_frame,
                from_=0,
                to=max(10, initial * 2),
                number_of_steps=100,
                command=lambda value, idx=i: self.on_slider_change(value, idx)
            )
            slider.set(initial)
            slider.grid(row=i, column=1, padx=5, pady=5)
            self.sliders.append(slider)
            
            value_label = ctk.CTkLabel(self.param_frame, text=f"{initial:.2f}")
            value_label.grid(row=i, column=2, padx=5, pady=5)
            self.value_labels.append(value_label)

    def on_slider_change(self, value, idx):
        self.value_labels[idx-1].configure(text=f"{float(value):.2f}")
        self.update_plot()

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        self.line = None
        self.bars = None

    def update_dist(self, _):
        selected_name = self.selector.get()
        for dist in DISTRIBUTIONS.values():
            if dist.name == selected_name:
                self.current_dist = dist
                break
        self.create_sliders()
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        params = [slider.get() for slider in self.sliders]
        dist = self.current_dist
        

        if dist.is_discrete:
            x = np.arange(int(dist.view_range[0]), int(dist.view_range[1]) + 1)
            y = dist.dist.pmf(x, *params)
            self.ax.bar(x, y, alpha=0.7, color='blue')
        else:
            x = np.linspace(dist.view_range[0], dist.view_range[1], 200)
            y = dist.dist.pdf(x, *params)
            self.ax.plot(x, y, 'b-')
            self.ax.fill_between(x, y, alpha=0.3)

        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Values')
        self.ax.set_ylabel('Probability')
        self.ax.set_title(f'{dist.name} Distribution')
        self.canvas.draw()

if __name__ == "__main__":
    DistributionVisualizer()
