def get_cron(repeat):
    if repeat == "never":
        return "@once"  
    elif repeat == "daily":
        return "0 0 * * *" 
    elif repeat == "weekly":
        return "0 0 * * 0"  
    elif repeat == "monthly":
        return "0 0 1 * *" 
    elif repeat == "yearly":
        return "0 0 1 1 *"
    else:
        raise ValueError(f"Unknown repeat type: {repeat}")