import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats

class CalculatorWindow(ctk.CTkToplevel):
    def __init__(self, dist):
        super().__init__()
        self.title(f"{dist.name} Calculator")
        self.geometry("800x800")
        self.dist = dist
        self.param_entries = []
        self.create_gui()
        self.setup_plot()

    def create_gui(self):
        input_fr = ctk.CTkFrame(self)
        input_fr.pack(pady=10, padx=10, fill='x')

        # Input section for parameters
        param_fr = ctk.CTkFrame(input_fr)
        param_fr.pack(pady=5, padx=5, fill='x')
        
        for i, param in enumerate(self.dist.params):
            ctk.CTkLabel(param_fr, text=param + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = ctk.CTkEntry(param_fr)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, str(self.dist.initial_values[i]))
            self.param_entries.append(entry)

        # Set calculation type
        calc_fr = ctk.CTkFrame(input_fr)
        calc_fr.pack(pady=5, padx=5, fill='x')
        
        ctk.CTkLabel(calc_fr, text="Calculate:").pack(pady=5)
        
        self.calc_type = ctk.StringVar(value="probability")
        self.calc_combobox = ctk.CTkComboBox(calc_fr, values=["Find P(X < x)", "Find x given P(X < x)"], 
                                              variable=self.calc_type, command=self.update_val_label)
        self.calc_combobox.pack(pady=5)

        # Frame for input val
        val_fr = ctk.CTkFrame(input_fr)
        val_fr.pack(pady=5, padx=5, fill='x')
        
        self.val_label = ctk.CTkLabel(val_fr, text="Enter x:")
        self.val_label.pack(side='left', padx=5)
        self.val_entry = ctk.CTkEntry(val_fr)
        self.val_entry.pack(side='left', padx=5)

        # Calculate button
        ctk.CTkButton(input_fr, text="Calculate", command=self.calculate).pack(pady=10)
        
        # Result display
        self.result_label = ctk.CTkLabel(input_fr, text="")
        self.result_label.pack(pady=10)

        # Create a frame to display the LaTeX equations for PDF and CDF
        latex_fr = ctk.CTkFrame(self)
        latex_fr.pack(pady=10, padx=10, fill='x')

        self.pdf_label = ctk.CTkLabel(latex_fr, text="", justify="left", anchor="w")
        self.pdf_label.pack(pady=5, padx=5)

        self.cdf_label = ctk.CTkLabel(latex_fr, text="", justify="left", anchor="w")
        self.cdf_label.pack(pady=5, padx=5)

    def setup_plot(self):
        plot_fr = ctk.CTkFrame(self)
        plot_fr.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_fr)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.update_plot()

    def update_val_label(self, event=None):
        calc_type = self.calc_type.get()
        if calc_type == "Find P(X < x)":
            self.val_label.configure(text="Enter x:")
        elif calc_type == "Find x given P(X < x)":
            self.val_label.configure(text="Enter probability (0-1):")

    def update_plot(self, x_value=None, probability=None):
        # Create a blank view
        self.ax.clear()
        
        try:
            params = [float(entry.get()) for entry in self.param_entries]
            dist = self.dist.dist
            
            # Set LaTeX equations for PDF and CDF
            pdf_form = self.dist.pdf
            cdf_form = self.dist.cdf
            self.pdf_label.configure(text=rf"PDF: {pdf_form}")
            self.cdf_label.configure(text=rf"CDF: {cdf_form}")

            if self.dist.is_discrete:
                # Discrete dist plot (PMF)
                x = np.arange(int(self.dist.view_range[0]), int(self.dist.view_range[1]) + 1)
                y = dist.pmf(x, *params)
                self.ax.bar(x, y, alpha=0.3, color='blue', label='PDF')

                if x_value is not None:
                    # Highlight bars for discrete dist
                    picked = x < x_value
                    self.ax.bar(x[picked], y[picked], alpha=0.5, color='green', label='P(X < x)')
                    self.ax.axvline(x=x_value, color='red', linestyle='--', label='x')

            else:
                # Continuous dist plot (PDF)
                x = np.linspace(self.dist.view_range[0], self.dist.view_range[1], 200)
                y = dist.pdf(x, *params)
                self.ax.plot(x, y, 'b-', label='PDF')

                if x_value is not None:
                    # Fill the chosen part
                    x_fill = x[x <= x_value]
                    y_fill = y[x <= x_value]
                    self.ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', label='P(X < x)')
                    self.ax.fill_between(x[x > x_value], y[x > x_value], alpha=0.3, color='red')
                    self.ax.axvline(x=x_value, color='red', linestyle='--', label='x')

            self.ax.grid(True, alpha=0.3)
            self.ax.set_xlabel('Values')
            self.ax.set_ylabel('Probability Density')

            self.ax.legend()
            self.canvas.draw()
            
        except ValueError:
            pass 

    def calculate(self):
        try:
            params = [float(entry.get()) for entry in self.param_entries]
            calc_type = self.calc_type.get()
            val = float(self.val_entry.get())
            
            dist = self.dist.dist
            
            if calc_type == "Find P(X < x)":
                if self.dist.is_discrete:
                    result = dist.cdf(val, *params)
                else:
                    result = dist.cdf(val, *params)
                self.result_label.configure(text=f"P(X < {val}) = {result:.4f}")
                self.update_plot(x_value=val, probability=result)
                
            elif calc_type == "Find x given P(X < x)":
                if val < 0 or val > 1:
                    raise ValueError("Probability must be between 0 and 1")
                if self.dist.is_discrete:
                    result = dist.ppf(val, *params)
                    result = int(np.ceil(result))
                else:
                    result = dist.ppf(val, *params)
                self.result_label.configure(text=f"x where P(X < x) = {val} is {result:.4f}")
                self.update_plot(x_value=result, probability=val)
                
        except ValueError as e:
            self.result_label.configure(text=f"Error: {str(e)}")
        except Exception as e:
            self.result_label.configure(text="Error in calculation")
