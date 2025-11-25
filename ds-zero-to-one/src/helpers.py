#helpers.py

import json, sys, platform, subprocess, os
from datetime import datetime
from pathlib import Path


# Add this line near the top of src/helpers.py
import plotly.graph_objects as go
# If you use plt or sns directly in helpers.py, you would need these too:
# import matplotlib.pyplot as plt
# import seaborn as sns

def save_plot_ts(fig, filename, scale=2, dpi=300, tight=True, timestamp_format="%Y-%m-%d_%H%M"):
    """
    Save a Matplotlib/Seaborn or Plotly figure with an automatic timestamp.
    
    Args:
        fig: Matplotlib Axes/Figure or Plotly Figure.
        filename (str): Base filename (e.g. '../reports/figures/tip_pct_smoker_dow_boxplot.png')
        scale (int): Scale factor for Plotly image export.
        dpi (int): Dots per inch for Matplotlib saves.
        tight (bool): Apply bbox_inches='tight' for Matplotlib saves.
        timestamp_format (str): datetime format for timestamp.
    
    Returns:
        Path to the saved image file.
    """
    path = Path(filename)
    timestamp = datetime.now().strftime(timestamp_format)
    
    # Split filename into stem + suffix and append timestamp
    outpath = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Plotly figure
        if isinstance(fig, go.Figure):
            fig.write_image(str(outpath), scale=scale)
            print(f"✅ Saved Plotly figure to: {outpath}")
        # Matplotlib Figure
        elif hasattr(fig, 'savefig'):
            fig.savefig(str(outpath), dpi=dpi, bbox_inches='tight' if tight else None)
            print(f"✅ Saved Matplotlib figure to: {outpath}")
        # Seaborn Axes
        elif hasattr(fig, 'get_figure'):
            fig.figure.savefig(str(outpath), dpi=dpi, bbox_inches='tight' if tight else None)
            print(f"✅ Saved Seaborn Axes figure to: {outpath}")
        else:
            raise TypeError("Unsupported figure type")
    except Exception as e:
        print(f"❌ Failed to save figure: {e}")
        return None
    
    return outpath


def _safe_git_info(repo_dir: str | Path = "."):
    """Return git commit hash and branch if available; otherwise None."""
    try:
        def run(cmd):
            return subprocess.check_output(cmd, cwd=repo_dir).decode().strip()
        commit = run(["git", "rev-parse", "HEAD"])
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return {"git_commit": commit, "git_branch": branch}
    except Exception:
        return {}

def _pandas_df_info(df):
    """Summarize a pandas DataFrame (shape + column dtypes) without dumping data."""
    try:
        return {
            "shape": tuple(df.shape),
            "columns": list(df.columns),
            "dtypes": {c: str(df.dtypes[c]) for c in df.columns},
        }
    except Exception:
        return None

def log_plot_metadata(
    image_path: str | Path,
    *,
    df=None,
    chart_type: str | None = None,
    library: str | None = None,          # 'matplotlib' | 'seaborn' | 'plotly'
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,            # plotly
    hue: str | None = None,              # seaborn
    group: str | None = None,
    trendline: str | None = None,        # e.g., 'ols'
    filters: dict | None = None,         # any filters applied to data
    dataset_name: str | None = None,     # friendly label
    dataset_path: str | None = None,     # data source path/URL
    notebook: str | None = None,         # e.g., 'notebooks/Study_Session_3.ipynb'
    notes: str | None = None,            # free-text notes
) -> Path:
    """
    Write a JSON sidecar next to the image with reproducibility metadata.
    Returns the JSON path.
    """
    image_path = Path(image_path)
    meta_path = image_path.with_suffix(".json")

    meta = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "image_file": str(image_path),
        "chart_type": chart_type,
        "library": library,
        "mapping": {"x": x, "y": y, "color": color, "hue": hue, "group": group},
        "modeling": {"trendline": trendline},
        "data": {
            "dataset_name": dataset_name,
            "dataset_path": dataset_path,
            "filters": filters or {},
            "frame_summary": _pandas_df_info(df) if df is not None else None,
        },
        "execution_env": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "conda_prefix": os.environ.get("CONDA_PREFIX"),
            "working_dir": str(Path.cwd()),
        },
        "source": {"notebook": notebook} if notebook else {},
        "vcs": _safe_git_info(),
        "notes": notes,
    }

    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"📝 Logged metadata → {meta_path}")
    return meta_path

def save_and_log_plot(
    fig,
    filename: str,
    *,
    df=None,
    chart_type: str | None = None,
    library: str | None = None,
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    hue: str | None = None,
    group: str | None = None,
    trendline: str | None = None,
    filters: dict | None = None,
    dataset_name: str | None = None,
    dataset_path: str | None = None,
    notebook: str | None = None,
    notes: str | None = None,
    timestamped: bool = True,
    **save_kwargs,   # forwarded to save_plot_ts/save_plot
):
    """
    Save a figure (Plotly or Matplotlib/Seaborn) and write a JSON sidecar with metadata.
    Returns (image_path, json_path).
    """
    # Use your save helpers defined earlier:
    if timestamped:
        outpath = save_plot_ts(fig, filename, **save_kwargs)
    else:
        # Non-timestamped variant
        outpath = Path(filename)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        # Decide write method based on type
        try:
            import plotly.graph_objects as go
            if isinstance(fig, go.Figure):
                fig.write_image(str(outpath), scale=save_kwargs.get("scale", 2))
            elif hasattr(fig, "savefig"):
                fig.savefig(str(outpath), dpi=save_kwargs.get("dpi", 300),
                            bbox_inches="tight" if save_kwargs.get("tight", True) else None)
            elif hasattr(fig, "get_figure"):
                fig.figure.savefig(str(outpath), dpi=save_kwargs.get("dpi", 300),
                                   bbox_inches="tight" if save_kwargs.get("tight", True) else None)
        except Exception as e:
            print(f"❌ Failed to save figure: {e}")
            return None, None

    json_path = log_plot_metadata(
        outpath,
        df=df,
        chart_type=chart_type,
        library=library,
        x=x,
        y=y,
        color=color,
        hue=hue,
        group=group,
        trendline=trendline,
        filters=filters,
        dataset_name=dataset_name,
        dataset_path=dataset_path,
        notebook=notebook,
        notes=notes,
    )
    return outpath, json_path

import difflib
from IPython.display import HTML, display

def show_diff(cell_a: str, cell_b: str, name_a="Cell A", name_b="Cell B", color=True):
    """
    Display a unified diff and (optionally) a colorized HTML diff between two code cells.

    Args:
        cell_a (str): Code text of the first cell
        cell_b (str): Code text of the second cell
        name_a (str): Label for the first cell (default: "Cell A")
        name_b (str): Label for the second cell (default: "Cell B")
        color (bool): Whether to show a colorized HTML diff (default: True)
    """
    # --- Plain unified diff (git-style text) ---
    diff = difflib.unified_diff(
        cell_a.splitlines(),
        cell_b.splitlines(),
        fromfile=name_a,
        tofile=name_b,
        lineterm=""
    )
    print("".join(f"{line}\n" for line in diff))
    
    # --- Optional pretty HTML diff ---
    if color:
        diff_html = difflib.HtmlDiff().make_file(
            cell_a.splitlines(), cell_b.splitlines(), fromdesc=name_a, todesc=name_b
        )
        display(HTML(diff_html))

# --- 1. Import libraries ---
import os
import sys
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#TODO: fix this
def setProjRoot(): #Doesn't work ... 
    # Manually define the correct project root path based on your previous output
    CORRECT_PROJECT_ROOT = "/home/rtackett/projects/Masters-level-DIY-Data-Science-Curriculum-ai-Era-/ds-zero-to-one"
    
    # Set CWD
    try:
        os.chdir(CORRECT_PROJECT_ROOT)
        print(f"✅ CWD successfully set to: {os.getcwd()}")
    
        # Add to sys.path for module imports (src.helpers)
        if CORRECT_PROJECT_ROOT not in sys.path:
            sys.path.append(CORRECT_PROJECT_ROOT)
            print("✅ Added project root to sys.path.")
    
    except FileNotFoundError:
        print("❌ CRITICAL ERROR: The manually defined project path does not exist.")
        sys.exit(1)


def calculate_vif(df, features):
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant

    X = df[features].copy()
    X = add_constant(X)

    vif_df = pd.DataFrame({
        "Feature": X.columns,
        "VIF": [variance_inflation_factor(X.values, i)
                for i in range(X.shape[1])]
    })

    return vif_df[vif_df["Feature"] != "const"]
